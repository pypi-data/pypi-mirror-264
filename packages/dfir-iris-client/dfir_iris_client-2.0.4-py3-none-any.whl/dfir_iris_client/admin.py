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
import warnings
from typing import List, BinaryIO
from typing import Union
from deprecated import deprecated

from dfir_iris_client.helper.assets_type import AssetTypeHelper
from dfir_iris_client.customer import Customer
from dfir_iris_client.helper.authorization import Permissions, CaseAccessLevel
from dfir_iris_client.helper.case_classifications import CaseClassificationsHelper
from dfir_iris_client.helper.ioc_types import IocTypeHelper
from dfir_iris_client.helper.report_template_types import ReportTemplateType, ReportTemplateLanguage
from dfir_iris_client.helper.utils import ApiResponse, ClientApiError, get_data_from_resp, parse_api_data, ClientApiData


class AdminHelper(object):
    """Handles administrative tasks"""

    def __init__(self, session):
        """
        Overlay offering administrative tasks. Initialisation of the class does NOT check if the calling user
        has admin rights anymore. If the user doesn't, 403 will be generated upon requests

        Args:
            session: ClientSession object

        """
        self._s = session

    @deprecated('Use the new has_permission(<permission>) method', version="2.0.0", action="error")
    def is_user_admin(self) -> bool:
        """
        Deprecated in IRIS v1.5.0. Use the new has_permission(<permission>) method.
        Returns True if the calling user is administrator

        Args:

        Returns:
            Bool - true if the calling is administrator

        """
        req = self._s.pi_get('user/is-admin')
        return req.is_success()

    def has_permission(self, permission: Permissions) -> ApiResponse:
        """
        Returns true if the user has the given permissions

        Args:
            permission: Permission to check

        Returns:
            ApiResponse
        """
        body = {
            "permission_name": permission.name,
            "permission_value": permission.value
        }

        req = self._s.pi_post('user/has-permission', data=body, cid=1)
        return req

    def get_user(self, user: Union[int, str], **kwargs) -> ApiResponse:
        """Return a user data

        Args:
          user: User ID or login of the user to get

        Returns:
          ApiResponse object
        """
        if kwargs.get('user_id') is not None:
            warnings.warn("\'user_id\' argument is deprecated, use \'user\' instead",
                          DeprecationWarning)
            user = kwargs.get('user_id')

        if isinstance(user, str):
            ret = self._s.pi_get(f'manage/users/lookup/login/{user}')
            if ret.is_error():
                return ret
            data = get_data_from_resp(ret)
            user = parse_api_data(data, 'user_id')

        return self._s.pi_get(f'manage/users/{user}')

    def add_user(self, login: str, name: str, password: str, email: str, is_service_account: bool = False,
                 **kwargs) -> ApiResponse:
        """
        Adds a new user. A new user can be successfully added if
        
        - login is unique
        - email is unique
        - password meets the requirements of IRIS
        
        !!! tip "Requires server administrator rights"

        Args:
          login: Username (login name) of the user to add
          name: Full name of the user
          password: Password of the user
          email: Email of the user
          is_service_account: True if the user is a service account

        Returns:
          ApiResponse

        """
        body = {
            "user_login": login,
            "user_name": name,
            "user_password": password,
            "user_email": email,
            "user_is_service_account": is_service_account,
            "cid": 1
        }

        if kwargs.get('is_admin') is not None:
            warnings.warn("\'is_admin argument\' is deprecated, use set_group_permissions method instead",
                          DeprecationWarning)

        return self._s.pi_post(f'manage/users/add', data=body)

    def deactivate_user(self, user: [int, str] = None) -> ApiResponse:
        """
        Deactivate a user from its user ID or login. Disabled users can't log in interactively nor user their API keys.
        They do not appear in proposed user lists.

        Args:
          user: User ID or login to deactivate

        Returns:
          ApiResponse object

        """
        user_id = None
        if isinstance(user, int):
            user_id = user

        elif isinstance(user, str):
            user_lookup_r = self._s.pi_get(f'manage/users/lookup/login/{user}', cid=1)
            if user_lookup_r.is_error():
                return ClientApiError(msg=user_lookup_r.get_msg())

            user_id = user_lookup_r.get_data().get('user_id')

        if user_id is None:
            return ClientApiError(msg="Invalid user ID or login")

        return self._s.pi_get(f'manage/users/deactivate/{user_id}')

    def update_user(self,
                    user: Union[int, str],
                    login: str = None,
                    name: str = None,
                    password: str = None,
                    email: str = None,
                    **kwargs) -> ApiResponse:
        """
        Updates a user. The user can be updated if :
        
        - login is unique
        - email is unique
        - password meets the requirements of IRIS
        
        Only set the parameters that needs to be updated.


        Args:
          user: User ID or login to update
          login: Login of the user
          name: Full name of the user
          password: Password of the user
          email: Email of the user

        Returns:
          ApiResponse

        """

        if kwargs.get('is_admin') is not None:
            warnings.warn("\'is_admin\' argument is deprecated, use set_group_permissions method instead",
                          DeprecationWarning)

        user_req = None
        if isinstance(user, int):
            user_req = self._s.pi_get(f'manage/users/{user}')

        elif isinstance(user, str):
            user_req = self.get_user(user=user)

        if user_req.is_error():
            return ClientApiError(msg=f'Unable to fetch user {user} for update',
                                  error=user_req.get_msg())

        user = user_req.get_data()

        body = {
            "user_login": login,
            "user_name": name if name else user.get('user_name'),
            "user_email": email if email else user.get('user_email'),
            "user_password": password if password else "",
            "cid": 1
        }

        return self._s.pi_post(f'manage/users/update/{user.get("user_id")}', data=body)

    def delete_user(self, user: [int, str], **kwargs) -> ApiResponse:
        """
        Deletes a user based on its login. A user can only be deleted if it does not have any
        activities in IRIS. This is to maintain coherence in the database. The user needs to be
        deactivated first.
        
        !!! tip "Requires administrative rights"

        Args:
          user: Username or user ID of the user to delete

        Returns:
          ApiResponse

        """

        if kwargs.get('login') is not None:
            warnings.warn("\'login\' argument is deprecated, use \'user\' instead",
                          DeprecationWarning)
            user = kwargs.get('login')

        if isinstance(user, int):
            return self.delete_user_by_id(user_id=user)

        if user is None:
            return ClientApiError(msg='Invalid user ID or login')

        user_req = self.get_user(user=user)
        if user_req.is_error():
            return ClientApiError(msg=f'Unable to fetch user {user} for update',
                                  error=user_req.get_msg())

        user = user_req.get_data()

        return self.delete_user_by_id(user_id=user.get('user_id'))

    def delete_user_by_id(self, user_id: int) -> ApiResponse:
        """
        Delete a user based on its ID. A user can only be deleted if it does not have any
        activities in IRIS. This is to maintain coherence in the database.


        Args:
          user_id: UserID of the user to delete

        Returns:
          ApiResponse

        """

        return self._s.pi_post(f'manage/users/delete/{user_id}', cid=1)

    def update_user_cases_access(self, user: Union[int, str], cases_list: List[int],
                                 access_level: CaseAccessLevel) -> ApiResponse:
        """
        Updates the cases that a user can access.

        

        Args:
          user: User ID or login to update
          cases_list: List of case IDs
          access_level: Access level to set for the user

        Returns:
          ApiResponse

        """
        user_req = self.get_user(user=user)

        if user_req.is_error():
            return ClientApiError(msg=f'Unable to fetch user {user} for update',
                                  error=user_req.get_msg())

        if not isinstance(cases_list, list):
            return ClientApiError(msg=f'Invalid cases list. Expected list of IDs')

        if not all(isinstance(case_id, int) for case_id in cases_list):
            return ClientApiError(msg=f'Invalid cases list. Expected list of IDs')

        if access_level not in CaseAccessLevel:
            return ClientApiError(msg=f'Invalid access level. Expected enum from CaseAccessLevel')

        user = parse_api_data(user_req.get_data(), 'user_id')

        body = {
            "access_level": access_level.value,
            "cases_list": cases_list,
            "cid": 1
        }

        return self._s.pi_post(f'manage/users/{user}/cases-access/update', data=body)

    def get_user_cases_access_trace(self, user: Union[int, str]) -> ApiResponse:
        """
        Get the trace of the cases access of a user.

        Args:
            user: User ID or login to update

        Returns:
            ApiResponse
        """
        user_req = self.get_user(user=user)

        if user_req.is_error():
            return ClientApiError(msg=f'Unable to fetch user {user} for update',
                                  error=user_req.get_msg())

        user = parse_api_data(user_req.get_data(), 'user_id')

        return self._s.pi_get(f'manage/access-control/audit/users/{user}')

    def recompute_user_cases_access(self, user: Union[int, str]) -> ApiResponse:
        """
        Recompute the cases access of a user.

        Args:
            user: User ID or login to update

        Returns:
            ApiResponse
        """
        user_req = self.get_user(user=user)

        if user_req.is_error():
            return ClientApiError(msg=f'Unable to fetch user {user} for update',
                                  error=user_req.get_msg())

        user = parse_api_data(user_req.get_data(), 'user_id')

        return self._s.pi_get(f'manage/access-control/recompute-effective-user-ac/{user}')

    def recompute_all_users_cases_access(self) -> ApiResponse:
        """
        Recompute the cases access of all users.

        Returns:
            ApiResponse object
        """
        return self._s.pi_get(f'manage/access-control/recompute-effective-users-ac')

    def add_ioc_type(self, name: str, description: str, taxonomy: str = None) -> ApiResponse:
        """
        Add a new IOC Type.


        Args:
          name: Name of the IOC type
          description: Description of the IOC type
          taxonomy: Taxonomy of the IOC Type

        Returns:
          ApiResponse

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


        Args:
          ioc_type_id: IOC type to delete

        Returns:
          ApiResponse

        """
        return self._s.pi_post(f'manage/ioc-types/delete/{ioc_type_id}', cid=1)

    def update_ioc_type(self, ioc_type_id: int, name: str = None,
                        description: str = None, taxonomy: str = None) -> ApiResponse:
        """
        Updates an IOC type. `ioc_type_id` needs to be a valid existing IocType ID.


        Args:
          ioc_type_id: IOC type to update
          name: Name of the IOC type
          description: Description of the IOC type
          taxonomy: Taxonomy of the IOC Type

        Returns:
          ApiResponse

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

    @deprecated(reason='This method is deprecated in IRIS > v1.4.3', action="error", version="2.0.0")
    def add_asset_type(self, name: str, description: str) -> ApiResponse:
        """
        Add a new Asset Type.


        Args:
          name: Name of the Asset type
          description: Description of the Asset type

        Returns:
          ApiResponse

        """
        body = {
            "asset_name": name,
            "asset_description": description,
            "cid": 1
        }
        return self._s.pi_post(f'manage/asset-type/add', data=body)

    def add_case_classification(self, name: str, name_expanded: str, description: str) -> ApiResponse:
        """ Add a new Case Classification.

        

        Args:
            name: Name of the Case Classification
            name_expanded: Expanded name of the Case Classification
            description: Description of the Case Classification


        Returns:
            ApiResponse
        """
        body = {
            "name": name,
            "name_expanded": name_expanded,
            "description": description,
            "cid": 1
        }
        return self._s.pi_post(f'manage/case-classifications/add', data=body)

    def delete_case_classification(self, case_classification_id: int) -> ApiResponse:
        """ Delete an existing Case Classification by its ID.

        

        Args:
            case_classification_id: Case Classification to delete

        Returns:
            ApiResponse
        """
        return self._s.pi_post(f'manage/case-classifications/delete/{case_classification_id}', cid=1)

    def update_case_classification(self, classification_id: int, name: str = None,
                                   name_expanded: str = None, description: str = None) -> ApiResponse:
        """ Updates a Case Classification. `case_classification_id` needs to be a valid existing CaseClassification ID.

        

        Args:
            classification_id: Case Classification to update
            name: Name of the Case Classification
            name_expanded: Expanded name of the Case Classification
            description: Description of the Case Classification

        Returns:
            ApiResponse
        """
        cch = CaseClassificationsHelper(session=self._s)

        case_classification_req = cch.get_case_classification(case_classification_id=classification_id)

        if case_classification_req.is_error():
            return ClientApiError(msg=f'Unable to fetch case classification #{classification_id} for update',
                                  error=case_classification_req.get_msg())

        case_classification = case_classification_req.get_data()

        body = {
            "name": name if name is not None else case_classification.get('name'),
            "name_expanded": name_expanded if name_expanded is not None else case_classification.get('name_expanded'),
            "description": description if description is not None else case_classification.get('description'),
            "cid": 1
        }

        return self._s.pi_post(f'manage/case-classifications/update/{classification_id}', data=body)

    def delete_asset_type(self, asset_type_id: int) -> ApiResponse:
        """
        Delete an existing asset type by its ID.

        Args:
          asset_type_id: Asset type to delete

        Returns:
          ApiResponse

        """
        return self._s.pi_post(f'manage/asset-type/delete/{asset_type_id}', cid=1)

    @deprecated(reason='This method is deprecated in IRIS > v1.4.3', action="error", version="2.0.0")
    def update_asset_type(self, asset_type_id: int, name: str = None,
                          description: str = None) -> ApiResponse:
        """
        Updates an Asset type. `asset_type_id` needs to be a valid existing AssetType ID.


        Args:
          asset_type_id: Asset type to update
          name: Name of the IOC type
          description: Description of the IOC type

        Returns:
          ApiResponse

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

    def add_customer(self, customer_name: str, customer_description: str = None,
                     customer_sla: str = None, custom_attributes: dict = {}) -> ApiResponse:
        """
        Creates a new customer. A new customer can be added if:
        
        - customer_name is unique

        Args:
            customer_name: Name of the customer to add.
            customer_description: Description of the customer
            customer_sla: SLA of the customer
            custom_attributes: Custom attributes of the customer

        Returns:
          ApiResponse object

        """
        body = {
            "customer_name": customer_name.lower(),
            "customer_description": customer_description,
            "customer_sla": customer_sla,
            "custom_attributes": custom_attributes
        }
        resp = self._s.pi_post('manage/customers/add',
                               data=body)
        return resp

    def update_customer(self, customer_id: int, customer_name: str):
        """
        Updates an existing customer. A customer can be updated if :
        
        - `customer_id` is a know customer ID in IRIS
        - `customer_name` is unique


        Args:
          customer_id: ID of the customer to update
          customer_name: Customer name

        Returns:
          ApiResponse object

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


        Args:
          customer: Customer name or customer ID

        Returns:
          ApiResponse object

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

        resp = self._s.pi_post(f'manage/customers/delete/{c_id}', cid=1)

        return resp

    def add_group(self, group_name: str, group_description: str, group_permissions: List[Permissions]) -> ApiResponse:
        """
        Add a new group with permissions. Cases access and members can be set later on with
        `set_group_access` and `set_group_members` methods. Permissions must be a list of known
        permissions from the Permission enum.

        Args:
            group_name: Name of the group
            group_description: Description of the group
            group_permissions: List of permission from Permission enum

        Returns:
            ApiResponse object
        """
        for perm in group_permissions:
            if not isinstance(perm, Permissions):
                return ClientApiError(msg=f'Invalid permission {perm}')

        body = {
            "group_name": group_name,
            "group_description": group_description,
            "group_permissions": [perm.value for perm in group_permissions],
            "cid": 1
        }

        return self._s.pi_post('manage/groups/add', data=body)

    def get_group(self, group: Union[str, int]) -> ApiResponse:
        """
        Get a group by its ID or name.

        Args:
            group: Group ID or group name

        Returns:
            ApiResponse object
        """
        if isinstance(group, str):
            lookup = self.lookup_group(group_name=group)
            if lookup.is_error():
                return lookup

            group = lookup.get_data().get('group_id')

        return self._s.pi_get(f'manage/groups/{group}', cid=1)

    def update_group(self, group: Union[str, int], group_name: str = None, group_description: str = None,
                     group_permissions: List[Permissions] = None) -> ApiResponse:
        """
        Update a group. Cases access and members can be with
        `set_group_access` and `set_group_members` methods. Permissions must be a list of known
        permissions from the Permission enum.

        Args:
            group: Group ID or group name
            group_name: Name of the group
            group_description: Description of the group
            group_permissions: List of permission from Permission enum

        Returns:
            ApiResponse object
        """
        if isinstance(group, str):
            lookup = self.lookup_group(group_name=group)
            if lookup.is_error():
                return lookup

            group = lookup.get_data().get('group_id')

        group_resp = self.get_group(group)
        if group_resp.is_error():
            return group_resp

        group_data = group_resp.get_data()

        group_perms = []
        if group_permissions is not None:
            for perm in group_permissions:
                if not isinstance(perm, Permissions):
                    return ClientApiError(msg=f'Invalid permission {perm}')
                group_perms.append(perm.value)

        else:
            perms = parse_api_data(group_data, 'group_permissions')
            for perm in perms:
                group_perms.append(perm.get('value'))

        group_description = group_description if group_description is not None \
            else parse_api_data(group_data, 'group_description')

        group_name = group_name if group_name is not None \
            else parse_api_data(group_data, 'group_name')

        body = {
            "group_name": group_name,
            "group_description": group_description,
            "group_permissions": group_perms,
            "cid": 1
        }

        return self._s.pi_post(f'manage/groups/update/{group}', data=body)

    def update_group_members(self, group: Union[str, int], members: List[int]) -> ApiResponse:
        """
        Update the members of a group. Members must be a list of user IDs.

        Args:
            group: Group ID or group name
            members: List of user IDs

        Returns:
            ApiResponse object
        """
        if isinstance(group, str):
            lookup = self.lookup_group(group_name=group)
            if lookup.is_error():
                return lookup

            group = lookup.get_data().get('group_id')

        if not isinstance(members, list):
            return ClientApiError(msg=f'Members must be a list of user IDs')

        if not all(isinstance(member, int) for member in members):
            return ClientApiError(msg=f'Members must be a list of user IDs')

        body = {
            "group_members": members,
            "cid": 1
        }

        return self._s.pi_post(f'manage/groups/{group}/members/update', data=body)

    def update_group_cases_access(self, group: Union[str, int], cases_list: List[int],
                                  access_level: CaseAccessLevel, auto_follow: bool = False) -> ApiResponse:
        """
        Update the cases access of a group. Cases access must be a list of case IDs. access_level must be
        a CaseAccessLevel enum.
        If auto_follow is True, the cases will be automatically added to the group when they are created.

        Args:
            group: Group ID or group name
            cases_list: List of case IDs
            access_level: CaseAccessLevel enum
            auto_follow: Set to true to auto follow cases new cases

        Returns:
            ApiResponse object
        """
        if isinstance(group, str):
            lookup = self.lookup_group(group_name=group)
            if lookup.is_error():
                return lookup

            group = lookup.get_data().get('group_id')

        if not isinstance(cases_list, list):
            return ClientApiError(msg=f'Cases access must be a list of case IDs')

        if not all(isinstance(case, int) for case in cases_list):
            return ClientApiError(msg=f'Cases access must be a list of case IDs')

        body = {
            "cases_list": cases_list,
            "access_level": access_level.value,
            "auto_follow": auto_follow,
            "cid": 1
        }

        return self._s.pi_post(f'manage/groups/{group}/cases-access/update', data=body)

    def delete_group(self, group: Union[str, int]) -> ApiResponse:
        """
        Delete a group by its ID or name.

        Args:
            group: Group ID or group name

        Returns:
            ApiResponse object
        """

        if isinstance(group, str):
            lookup = self.lookup_group(group_name=group)
            if lookup.is_error():
                return lookup

            group = lookup.get_data().get('group_id')

        return self._s.pi_post(f'manage/groups/delete/{group}', cid=1)

    def list_groups(self) -> ApiResponse:
        """
        List all groups.

        Returns:
            ApiResponse object
        """
        return self._s.pi_get('manage/groups/list', cid=1)

    def lookup_group(self, group_name: str) -> ApiResponse:
        """
        Lookup a group by its name.

        Args:
            group_name: Group name

        Returns:
            ApiResponse object
        """
        group_lists = self.list_groups()
        if group_lists.is_error():
            return group_lists

        for group in group_lists.get_data():
            if group.get('group_name').lower() == group_name.lower():
                response = ClientApiData(data=group)

                return ApiResponse(response=response, uri=group_lists.get_uri())

        return ClientApiError(msg=f'Group {group_name} not found')

    def add_report_template(self, template_name: str, template_description: str, template_type: ReportTemplateType,
                            template_name_format: str, template_language: ReportTemplateLanguage,
                            template_stream: BinaryIO) -> ApiResponse:
        """
        Add a new report template. template_type must be a ReportTemplateType enum.

        Args:
            template_name: Name of the template
            template_description: Description of the template
            template_type: ReportTemplateType enum
            template_language: ReportTemplateLanguage enum
            template_name_format: Name format of the template

            template_stream: Template data
            cid: Case ID

        Returns:
            ApiResponse object
        """
        files = {
            'file': template_stream
        }

        body = {
            "report_name": template_name,
            "report_type": template_type.value,
            "report_description": template_description,
            "report_language": template_language.value,
            "report_name_format": template_name_format,
            "cid": 1
        }

        return self._s.pi_post_files('manage/templates/add', data=body, files=files, cid=1)

    def delete_report_template(self, template_id: int) -> ApiResponse:
        """
        Delete a report template by its ID.

        Args:
            template_id: Template ID

        Returns:
            ApiResponse object
        """
        return self._s.pi_post(f'manage/templates/delete/{template_id}', cid=1)
