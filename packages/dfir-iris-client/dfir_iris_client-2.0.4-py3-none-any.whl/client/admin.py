#  IRIS Client API Source Code
#  contact@dfir-iris.org
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU Lesser General Public
#  License as published by the Free Software Foundation; either
#  version 3 of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
#  Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
from typing import Union

from helper.assets_type import AssetTypeHelper
from customer import Customer
from helper.ioc_types import IocTypeHelper
from helper.utils import ApiResponse, ClientApiError, get_data_from_resp, parse_api_data


class AdminHelper(object):
    """
    Handles administrative tasks
    """
    def __init__(self, session):
        """
        Overlay offering administrative tasks. Initialisation of the class checks if the calling user
        has admin rights. If the user doesn't, a ClientApiError exception is raised.

        :raises: ClientApiError if unprivileged user
        :param session: ClientSession object
        """
        self._s = session

        if not self.is_user_admin():
            raise Exception(ClientApiError('Only administrators can use AdminHelper'))

    def is_user_admin(self) -> bool:
        """
        Returns True if the calling user is administrator

        :return: Bool - true if the calling is administrator
        """
        req = self._s.pi_get('user/is-admin')
        return req.is_success()

    def get_user(self, login: str) -> ApiResponse:
        """
        Returns a user by its login. Login names are unique in Iris.

        :param login: username to lookup
        :return: ApiResponse
        """

        user_lookup_r = self._s.pi_get(f'manage/users/lookup/login/{login}', cid=1)
        if user_lookup_r.is_error():
            return ClientApiError(msg=user_lookup_r.get_msg())

        user_id = user_lookup_r.get_data().get('user_id')

        return self._s.pi_get(f'manage/users/{user_id}')

    def add_user(self, login: str, name: str, password: str, email: str, is_admin: bool= False) -> ApiResponse:
        """
        Adds a new user. A new user can be successfully added if

            - login is unique
            - email is unique
            - password meets the requirements of IRIS

        .. warning:: Requires admin rights

        :param login: Username (login name) of the user to add
        :param name: Full name of the user
        :param password: Password of the user
        :param email: Email of the user
        :param is_admin: Set to true if user is admin
        :return: ApiResponse
        """
        body = {
            "user_login": login,
            "user_name": name,
            "user_password": password,
            "user_email": email,
            "cid": 1
        }

        if is_admin:
            body['user_isadmin'] = "y"

        return self._s.pi_post(f'manage/users/add', data=body)

    def deactivate_user(self, user_id: int = None) -> ApiResponse:
        """
        Deactivate a user from its user ID. Disabled users can't login interactively nor user their API keys.
        They do not appears in proposed user lists.

        :param user_id: User ID to deactivate
        :return: ApiResponse object
        """
        return self._s.pi_get(f'manage/users/deactivate/{user_id}')

    def update_user(self, login: str = None,
                    name: str = None,
                    password: str = None,
                    email: str = None,
                    is_admin: bool = None) -> ApiResponse:
        """
        Updates a user. The user can be updated if :

            - login is unique
            - email is unique
            - password meets the requirements of IRIS

        Password can be left empty to update other attributes.

        .. warning:: Requires admin rights

        :param login: Username (login name) of the user to update
        :param name: Full name of the user
        :param password: Password of the user
        :param email: Email of the user
        :param is_admin: Set to true if user is admin
        :return: ApiResponse
        """

        user_req = self.get_user(login=login)
        if user_req.is_error():
            return ClientApiError(msg=f'Unable to fetch user {login} for update',
                                  error=user_req.get_msg())

        user = user_req.get_data()

        body = {
            "user_login": login,
            "user_name": name if name else user.get('user_name'),
            "user_email": email if email else user.get('user_email'),
            "user_password": password if password else "",
            "cid": 1
        }

        if is_admin:
            body['user_isadmin'] = "y"

        return self._s.pi_post(f'manage/users/update/{user.get("user_id")}', data=body)

    def delete_user(self, login: str) -> ApiResponse:
        """
        Deletes a user based on its login. A user can only be deleted if it does not have any
        activities in IRIS. This is to maintain coherence in the database.

        .. warning:: Requires admin rights

        :param login: Username (login name) of the user to delete
        :return: ApiResponse
        """
        user_req = self.get_user(login=login)
        if user_req.is_error():
            return ClientApiError(msg=f'Unable to fetch user {login} for update',
                                  error=user_req.get_msg())

        user = user_req.get_data()

        return self.delete_user_by_id(user_id=user.get('user_id'))

    def delete_user_by_id(self, user_id: int) -> ApiResponse:
        """
        Delete a user based on its ID. A user can only be deleted if it does not have any
        activities in IRIS. This is to maintain coherence in the database.

        .. warning:: Requires admin rights

        :param user_id: UserID of the user to delete
        :return: ApiResponse
        """

        return self._s.pi_get(f'manage/users/delete/{user_id}')

    def add_ioc_type(self, name: str, description: str, taxonomy: str = None) -> ApiResponse:
        """
        Add a new IOC Type.

        .. warning:: Requires admin rights

        :param name: Name of the IOC type
        :param description: Description of the IOC type
        :param taxonomy: Taxonomy of the IOC Type
        :return: ApiResponse
        """
        body = {
            "type_name": name,
            "type_description": description,
            "type_taxonomy": taxonomy if taxonomy else "",
            "cid": 1
        }
        return self._s.pi_post(f'manage/ioc-types/add', data=body)

    def delete_ioc_type(self, ioc_type_id: int) -> ApiResponse:
        """
        Delete an existing IOC Type by its ID.

        .. warning:: Requires admin rights

        :param ioc_type_id: IOC type to delete
        :return: ApiResponse
        """
        return self._s.pi_get(f'manage/ioc-types/delete/{ioc_type_id}')

    def update_ioc_type(self, ioc_type_id: int, name: str = None,
                        description: str = None, taxonomy: str = None) -> ApiResponse:
        """
        Updates an IOC type. `ioc_type_id` needs to be a valid existing IocType ID.

        .. warning:: Requires admin rights

        :param ioc_type_id: IOC type to update
        :param name: Name of the IOC type
        :param description: Description of the IOC type
        :param taxonomy: Taxonomy of the IOC Type
        :return: ApiResponse
        """

        ioc_type = IocTypeHelper(session=self._s)
        ioct_req = ioc_type.get_ioc_type(ioc_type_id=ioc_type_id)
        if ioct_req.is_error():
            return ClientApiError(msg=f'Unable to fetch ioc type #{ioc_type_id} for update',
                                  error=ioct_req.get_msg())

        ioc = ioct_req.get_data()

        body = {
            "type_name": name if name else ioc.get('type_name'),
            "type_description": description if description else ioc.get('type_description'),
            "type_taxonomy": taxonomy if taxonomy else ioc.get('type_taxonomy'),
            "cid": 1
        }
        return self._s.pi_post(f'manage/ioc-types/update/{ioc_type_id}', data=body)

    def add_asset_type(self, name: str, description: str) -> ApiResponse:
        """
        Add a new Asset Type.

        .. warning:: Requires admin rights

        :param name: Name of the Asset type
        :param description: Description of the Asset type
        :return: ApiResponse
        """
        body = {
            "asset_name": name,
            "asset_description": description,
            "cid": 1
        }
        return self._s.pi_post(f'manage/asset-type/add', data=body)

    def delete_asset_type(self, asset_type_id: int) -> ApiResponse:
        """
        Delete an existing asset type by its ID.

        .. warning:: Requires admin rights

        :param asset_type_id: Asset type to delete
        :return: ApiResponse
        """
        return self._s.pi_get(f'manage/asset-type/delete/{asset_type_id}')

    def update_asset_type(self, asset_type_id: int, name: str = None,
                          description: str = None) -> ApiResponse:
        """
        Updates an Asset type. `asset_type_id` needs to be a valid existing AssetType ID.

        .. warning:: Requires admin rights

        :param asset_type_id: Asset type to update
        :param name: Name of the IOC type
        :param description: Description of the IOC type
        :return: ApiResponse
        """

        asset_type = AssetTypeHelper(session=self._s)
        sat_req = asset_type.get_asset_type(asset_type_id=asset_type_id)
        if sat_req.is_error():
            return ClientApiError(msg=f'Unable to fetch asset type #{sat_req} for update',
                                  error=sat_req.get_msg())

        ioc = sat_req.get_data()

        body = {
            "asset_name": name if name else ioc.get('asset_name'),
            "asset_description": description if description else ioc.get('asset_description'),
            "cid": 1
        }
        return self._s.pi_post(f'manage/asset-type/update/{asset_type_id}', data=body)

    def add_customer(self, customer_name: str):
        """
        Creates a new customer. A new customer can be added if:

            - customer_name is unique

        .. warning:: Requires admin rights

        :param: str: Customer name
        :return: ApiResponse object
        """
        body = {
            "customer_name": customer_name.lower()
        }
        resp = self._s.pi_post('/manage/customers/add',
                               data=body)
        return resp

    def update_customer(self, customer_id: int, customer_name: str):
        """
        Updates an existing customer. A customer can be updated if :

            - `customer_id` is a know customer ID in IRIS
            - `customer_name` is unique

        .. warning:: Requires admin rights

        :param customer_id: ID of the customer to update
        :param customer_name: Customer name
        :return: ApiResponse object
        """
        body = {
            "customer_name": customer_name.lower()
        }
        resp = self._s.pi_post(f'/manage/customers/update/{customer_id}',
                               data=body)
        return resp

    def delete_customer(self, customer: Union[str, int]) -> ApiResponse:
        """
        Deletes a customer from its ID or name.

        .. warning:: Requires admin rights

        :param customer: Customer name or customer ID
        :return: ApiResponse object
        """
        if isinstance(customer, str):

            c = Customer(session=self._s)
            c_id = c.lookup_customer(customer_name=customer)

            if not c_id:
                return ClientApiError(f'Customer {customer} not found')

            data = get_data_from_resp(c_id)
            c_id = parse_api_data(data, 'customer_id')

        else:
            c_id = customer

        resp = self._s.pi_get(f'manage/customers/delete/{c_id}')

        return resp