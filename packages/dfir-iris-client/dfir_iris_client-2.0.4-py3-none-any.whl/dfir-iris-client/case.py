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
from customer import Customer
from admin import AdminHelper
from helper.assets_type import AssetTypeHelper
from helper.analysis_status import AnalysisStatusHelper
from helper.ioc_types import IocTypeHelper
from helper.events_categories import EventCategoryHelper
from helper.task_status import TaskStatusHelper
from users import User
from helper.tlps import TlpHelper
from helper.utils import ClientApiError, ApiResponse

from typing import Union, List
import datetime


class Case(object):
    """
    Handles the case methods
    """
    def __init__(self, session, case_id: int = None):
        self._s = session
        self._cid = case_id

    def list_cases(self) -> ApiResponse:
        """
        Returns a list of all the cases

        :return: ApiResponse
        """
        return self._s.pi_get('manage/cases/list')

    def get_case(self, cid: int) -> ApiResponse:
        """
        Gets an existing case from its ID

        :param cid: CaseID to fetch
        :return: ApiResponse object
        """
        return self._s.pi_get(f'manage/cases/{cid}')

    def add_case(self, case_name: str, case_description: str,
                 case_customer: Union[str, int], soc_id: str, create_customer=False) -> ApiResponse:
        """
        Creates a new case. If create_customer is set to true and the customer doesn't exist,
        it is created. Otherwise an error is returned.

        :param case_name: case_name
        :param case_description: Description of the case
        :param case_customer: Name or ID of the customer
        :param soc_id: SOC Number
        :param create_customer: Set to true to create the customer is doesn't exists.
        :return: ApiResponse object
        """
        if isinstance(case_customer, str):
            # Get the customer ID
            customer = Customer(session=self._s)
            c_id = customer.lookup_customer(customer_name=case_customer)

            if c_id.is_error():
                if create_customer:
                    adm = AdminHelper(self._s)
                    c_resp = adm.add_customer(customer_name=case_customer)
                    if c_resp.is_error():
                        return c_resp

                    c_id = c_resp

                else:

                    return ClientApiError(f'Customer {case_customer} wasn\'t found. Check syntax or set '
                                          f'create_customer flag to create it')

            if c_id.is_error():
                return c_id

            case_customer = c_id.get_data().get('customer_id')

        body = {
            "case_name": case_name,
            "case_customer": case_customer,
            "case_soc_id": soc_id,
            "case_description": case_description
        }
        resp = self._s.pi_post('manage/cases/add', data=body)

        return resp

    def delete_case(self, cid: int) -> ApiResponse:
        """
        Deletes a case based on its ID. All objects associated to the case are deleted. This includes :
            - assets,
            - iocs that are only referenced in this case
            - notes
            - summary
            - events
            - evidences
            - tasklogs

        :param cid: int - Case to delete
        :return: ApiResponse
        """
        resp = self._s.pi_get(f'manage/cases/delete/{cid}')

        return resp

    def case_id_exists(self, cid: int) -> bool:
        """
        Checks if a case id is valid by probing the summary endpoint.
        This method returns true if the probe was successful. If False is returned
        it might not indicate the case doesn't exist but might be the result of a request malfunction
        (server down, invalid API token, etc).

        :param cid: int - Case ID to check
        :return: True if case ID exists otherwise false
        """
        resp = self._s.pi_get(f'case/summary/fetch', cid=cid)
        return resp.is_success()

    def set_cid(self, cid: int) -> bool:
        """
        Sets the current cid for the Case instance.
        It can be override be setting the cid of each method though not recommended to keep consistency.

        :param cid: Case ID
        :return: Always true
        """

        self._cid = cid
        return True

    def _assert_cid(self, cid: int) -> int:
        """
        Verifies that the provided cid is set. This does not verify the validity of the cid.
        If an invalid CID is set, the requests are emitted but will likely fail.

        :raises: Exception is Case ID format is invalid
        :param cid: Case ID
        :return: CaseID as int
        """
        if not cid and not self._cid:
            raise Exception("No case ID provided. Either use cid argument or set_cid method")

        if not cid:
            cid = self._cid

        if not isinstance(cid, int):
            raise Exception(f'Invalid CID type. Got {type(cid)} but was expecting int')

        return cid

    def get_summary(self, cid: int = None) -> ApiResponse:
        """
        Returns the summary of the specified case id.

        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)
        return self._s.pi_get(f'case/summary/fetch', cid=cid)

    def set_summary(self, summary_content: str = None, cid: int = None) -> ApiResponse:
        """
        Sets the summary of the specified case id.

        .. warning:: This completely replace the current content of the summary. Any co-worker working on the summary
            will receive an overwrite order from the server. The order is immediately received by web socket. This method
            should probably be only used when setting a new case.

        :param cid: Case ID
        :param summary_content: Content of the summary to push. This will completely replace the current content
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)
        body = {
            "case_description": summary_content,
            "cid": cid
        }

        return self._s.pi_post('case/summary/update', data=body)

    def list_notes_groups(self, cid: int = None) -> ApiResponse:
        """
        Returns a list of notes groups of the target cid case

        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)
        return self._s.pi_get('case/notes/groups/list', cid=cid)

    def get_notes_group(self, group_id:int, cid: int = None) -> ApiResponse:
        """
        Returns a notes group based on its ID. The group ID needs to match the CID where it is stored.

        :param cid: Case ID
        :param group_id: Group ID to fetch
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/notes/groups/{group_id}', cid=cid)

    def add_notes_group(self, group_title: str = None, cid: int = None) -> ApiResponse:
        """
        Creates a new notes group in the target cid case.
        Group_title can be an existing group, there is no uniqueness.

        :param cid: Case ID
        :param group_title: Name of the group to add
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)
        body = {
            "group_title": group_title,
            "cid": cid
        }
        return self._s.pi_post('case/notes/groups/add', data=body)

    def update_notes_group(self, group_id: int, group_title: str, cid: int = None) -> ApiResponse:
        """
        Updates a notes group in the target cid case.
        `group_id` need to be an existing group in the target case.
        `group_title` can be an existing group, there is no uniqueness.

        :param cid: Case ID
        :param group_id: Group ID to update
        :param group_title: Name of the group
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)
        body = {
            "group_title": group_title,
            "group_id": group_id,
            "cid": cid
        }
        return self._s.pi_post('case/notes/groups/update', data=body)

    def delete_notes_group(self, group_id: int, cid: int = None) -> ApiResponse:
        """
         Deletes a notes group. All notes in the target groups are deleted ! There is not way to get the notes back.
         Case ID needs to match the case where the group is stored.

        :param cid: Case ID
        :param group_id: ID of the group
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)
        return self._s.pi_get(f'case/notes/groups/delete/{group_id}', cid=cid)

    def get_note(self, note_id: int, cid: int = None) -> ApiResponse:
        """
        Fetches a note. note_id needs to be a valid existing note in the target case.

        :param cid: Case ID
        :param note_id: ID of the note to fetch
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/notes/{note_id}', cid=cid)

    def update_note(self, note_id: int, note_title: str = None, note_content: str = None,
                    cid: int = None) -> ApiResponse:
        """
        Updates a note. note_id needs to be a valid existing note in the target case.
        Only the content of the set fields is replaced.


        :param cid: Case ID
        :param note_id: Name of the note to update
        :param note_content: Content of the note
        :param note_title: Title of the note
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        note_req = self.get_note(note_id=note_id, cid=cid)
        if note_req.is_error():
            return ClientApiError(f'Unable to fetch note #{note_id} for update', msg=note_req.get_msg())

        note = note_req.get_data()

        body = {
            "note_title": note_title if note_title else note.get('note_title'),
            "note_content": note_content if note_content else note.get('note_content'),
            "cid": cid
        }

        return self._s.pi_post(f'case/notes/update/{note_id}', data=body)

    def delete_note(self, note_id: int, cid: int = None) -> ApiResponse:
        """
         Deletes a note. note_id needs to be a valid existing note in the target case.

        :param cid: int - Case ID
        :param note_id: int - Name of the note to delete
        :return APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/notes/delete/{note_id}', cid=cid)

    def add_note(self, note_title: str, note_content: str, group_id: int, cid: int = None) -> ApiResponse:
        """
         Creates a new note. Case ID and group note ID need to match the case in which the note is stored.

        :param cid: Case ID
        :param note_title: Title of the note
        :param note_content: Content of the note
        :param group_id: Target group to attach the note to
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        body = {
            "note_title": note_title,
            "note_content": note_content,
            "group_id": group_id,
            "cid": cid
        }

        return self._s.pi_post(f'case/notes/add', data=body)

    def search_notes(self, search_term: str, cid: int = None) -> ApiResponse:
        """
         Searches in notes. Case ID and group note ID need to match the case in which the notes are stored.
         Only the titles and notes ID of the matching notes are return, not the actual content.
         Use % for wildcard.

        :param cid: int - Case ID
        :param search_term: str - Term to search in notes
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        body = {
            "search_term": search_term,
            "cid": cid
        }

        return self._s.pi_post(f'case/notes/search', data=body)

    def list_assets(self, cid: int = None) -> ApiResponse:
        """
        Returns a list of all assets of the target case.

        :param cid: int - Case ID
        :return: APIResponse
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get('case/assets/list', cid=cid)

    def add_asset(self, name: str, asset_type: Union[str, int], analysis_status: Union[str, int],
                  compromised: bool = None, tags: List[str] = None,
                  description: str = None, domain: str = None, ip: str = None, additional_info: str = None,
                  ioc_links: list = None, cid: int = None) -> ApiResponse:
        """
        Adds an asset to the target case id.

        If they are strings, asset_types and analysis_status are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.

        :param name: Name of the asset to add
        :param asset_type: Name or ID of the asset type
        :param description: Description of the asset
        :param domain: Domain of the asset
        :param ip: IP of the asset
        :param additional_info: Additional information,
        :param analysis_status: Status of the analysis
        :param compromised: Set to true if asset is compromised
        :param tags: List of tags
        :param ioc_links: List of IOC to link to this asset
        :param cid: int - Case ID
        :return: APIResponse
        """
        cid = self._assert_cid(cid)

        if isinstance(asset_type, str):
            ast = AssetTypeHelper(session=self._s)
            asset_type_r = ast.lookup_asset_type_name(asset_type_name=asset_type)

            if not asset_type_r:
                return ClientApiError(msg=f'Asset type {asset_type} was not found')

            else:
                asset_type = asset_type_r

        if isinstance(analysis_status, str):
            ant = AnalysisStatusHelper(self._s)
            analysis_status_r = ant.lookup_analysis_status_name(analysis_status_name=analysis_status)

            if not analysis_status_r:
                return ClientApiError(msg=f"Analysis status {analysis_status} was not found")

            else:
                analysis_status = analysis_status_r

        body = {
            "asset_name": name,
            "asset_type_id": asset_type,
            "analysis_status_id": analysis_status,
            "cid": cid
        }

        if description is not None:
            body['asset_description'] = description
        if domain is not None:
            body['asset_domain'] = domain
        if ip is not None:
            body['asset_ip'] = ip
        if additional_info is not None:
            body['asset_info'] = additional_info
        if ioc_links is not None:
            body['ioc_links'] = ioc_links
        if compromised is not None:
            body['asset_compromised'] = compromised
        if tags is not None:
            body['asset_tags'] = ','.join(tags)

        return self._s.pi_post(f'case/assets/add', data=body)

    def get_asset(self, asset_id: int, cid: int = None) -> ApiResponse:
        """
        Returns an asset information from its ID.

        :param asset_id: ID of the asset to fetch
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/assets/{asset_id}', cid=cid)

    def asset_exists(self, asset_id: int, cid: int = None) -> bool:
        """
        Returns true if asset_id exists in the context of the current case or cid.
        This method is an overlay of get_asset and thus not performant.

        :param asset_id: Asset to lookup
        :param cid: Case ID
        :return: True if exists else false
        """
        cid = self._assert_cid(cid)
        resp = self.get_asset(asset_id=asset_id, cid=cid)

        return resp.is_success()

    def update_asset(self, asset_id: int, name: str = None, asset_type: Union[str, int] = None, tags: List[str] = None,
                     analysis_status: Union[str, int] = None, description: str = None, domain: str = None,
                     ip: str = None, additional_info: str = None, ioc_links: list = None, compromised: bool = None,
                     cid: int = None, no_sync = False) -> ApiResponse:
        """
        Updates an asset. asset_id needs to be an existing asset in the target case cid.

        If they are strings, asset_types and analysis_status are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.

        :param asset_id: ID of the asset to update
        :param name: Name of the asset
        :param asset_type: Name or ID of the asset type
        :param tags: List of tags
        :param description: Description of the asset
        :param domain: Domain of the asset
        :param ip: IP of the asset
        :param additional_info: Additional information,
        :param analysis_status: Status of the analysis
        :param ioc_links: List of IOC to link to this asset
        :param compromised: True is asset is compromised
        :param cid: int - Case ID
        :return: APIResponse
        """
        cid = self._assert_cid(cid)

        asset = None
        if not no_sync:
            asset_req = self.get_asset(asset_id=asset_id, cid=cid)
            if asset_req.is_error():
                return asset_req

            asset = asset_req.get_data()

        if isinstance(asset_type, str):
            ast = AssetTypeHelper(session=self._s)
            asset_type_r = ast.lookup_asset_type_name(asset_type_name=asset_type)

            if not asset_type_r:
                return ClientApiError(msg=f'Asset type {asset_type} not found')

            else:
                asset_type = asset_type_r

        if isinstance(analysis_status, str):
            ant = AnalysisStatusHelper(self._s)
            analysis_status_r = ant.lookup_analysis_status_name(analysis_status_name=analysis_status)

            if not analysis_status_r:
                return ClientApiError(msg=f"Analysis status {analysis_status} not found")

            else:
                analysis_status = analysis_status_r

        if ioc_links:
            for link in ioc_links:
                ioc = self.get_ioc(ioc_id=int(link))
                if ioc.is_error():
                    return ClientApiError(msg=f"IOC {link} was not found", error=ioc.get_data())

        body = {
            "asset_name": name if name is not None or no_sync else asset.get('asset_name'),
            "asset_type_id": asset_type if asset_type is not None or no_sync else int(asset.get('asset_type_id')),
            "analysis_status_id": analysis_status if analysis_status is not None or no_sync else int(asset.get('analysis_status_id')),
            "asset_description": description if description is not None or no_sync else asset.get('analysis_status'),
            "asset_domain": domain if domain is not None or no_sync else asset.get('asset_domain'),
            "asset_ip": ip if ip is not None or no_sync else asset.get('asset_ip'),
            "asset_info": additional_info if additional_info is not None or no_sync else asset.get('asset_info'),
            "asset_compromised": compromised if compromised is not None or no_sync else asset.get('asset_compromise'),
            "asset_tags": ','.join(tags) if tags is not None or no_sync else asset.get('asset_tags'),
            "cid": cid
        }

        if ioc_links is not None:
            body['ioc_links'] = ioc_links

        return self._s.pi_post(f'case/assets/update/{asset_id}', data=body)

    def delete_asset(self, asset_id: int, cid: int = None) -> ApiResponse:
        """
        Deletes an asset identified by asset_id. CID must match the case in which the asset is stored.

        :param: asset_id: ID of the asset to remove
        :param: cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/assets/delete/{asset_id}', cid=cid)

    def list_iocs(self, cid: int = None) -> ApiResponse:
        """
        Returns a list of all iocs of the target case.

        :param: cid: Case ID
        :return: APIResponse
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get('case/ioc/list', cid=cid)

    def add_ioc(self, value: str, ioc_type: Union[str, int], description: str = None,
                ioc_tlp: Union[str, int] = None, ioc_tags: list = None, cid: int = None) -> ApiResponse:
        """
        Adds an ioc to the target case id.

        If they are strings, ioc_tlp and ioc_type are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.

        :param value: Value of the IOC
        :param ioc_type: Type of IOC, either name or type ID
        :param description: Optional - Description of the IOC
        :param ioc_tlp: TLP name or tlp ID. Default is orange
        :param ioc_tags: List of tags to add
        :param cid: Case ID
        :return: APIResponse
        """
        cid = self._assert_cid(cid)

        if ioc_tlp and isinstance(ioc_tlp, str):
            tlp = TlpHelper(session=self._s)
            ioc_tlp_r = tlp.lookup_tlp_name(tlp_name=ioc_tlp)

            if not ioc_tlp_r:
                return ClientApiError(msg=f"TLP {ioc_tlp} is invalid")

            ioc_tlp = ioc_tlp_r

        if ioc_type and isinstance(ioc_type, str):
            ioct = IocTypeHelper(session=self._s)
            ioct_r = ioct.lookup_ioc_type_name(ioc_type_name=ioc_type)

            if not ioct_r:
                return ClientApiError(msg=f"IOC type {ioc_type} is invalid", error=ioct_r)

            ioc_type = ioct_r

        if ioc_tags and not isinstance(ioc_tags, list):
            return ClientApiError(f"IOC tags must be a list of str")

        body = {
            "ioc_value": value,
            "ioc_tlp_id": ioc_tlp if ioc_tlp else 2,
            "ioc_type_id": ioc_type,
            "cid": cid
        }

        if description:
            body['ioc_description'] = description
        if ioc_tags:
            body['ioc_tags'] = ",".join(ioc_tags)

        return self._s.pi_post(f'case/ioc/add', data=body)

    def get_ioc(self, ioc_id: int, cid: int = None) -> ApiResponse:
        """
        Returns an IOC.  ioc_id needs to be an existing ioc in the provided case ID.

        :param ioc_id: IOC ID
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/ioc/{ioc_id}', cid=cid)

    def update_ioc(self, ioc_id: int, value: str = None, ioc_type: [str, int] = None, description: str = None,
                    ioc_tlp: Union[str, int] = None, ioc_tags: list = None, cid: int = None) -> ApiResponse:
        """
        Updates an existing IOC. ioc_id needs to be an existing ioc in the provided case ID.

        If they are strings, ioc_tlp and ioc_type are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.

        :param ioc_id: IOC ID to update
        :param value: Value of the IOC
        :param ioc_type: Type of IOC, either name or type ID
        :param description: Description of the IOC
        :param ioc_tlp: TLP name or tlp ID. Default is orange
        :param ioc_tags: List of tags to add
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        ioc_req = self.get_ioc(ioc_id, cid=cid)
        if ioc_req.is_error():
            return ClientApiError(msg=f'Unable to fetch IOC #{ioc_id} for update', error=ioc_req.get_msg())

        ioc = ioc_req.get_data()

        if ioc_tlp and isinstance(ioc_tlp, str):
            tlp = TlpHelper(session=self._s)
            ioc_tlp_r = tlp.lookup_tlp_name(tlp_name=ioc_tlp)

            if not ioc_tlp_r:
                return ClientApiError(msg=f"TLP {ioc_tlp} is invalid")

            ioc_tlp = ioc_tlp_r

        if ioc_type and isinstance(ioc_type, str):
            ioct = IocTypeHelper(session=self._s)
            ioct_r = ioct.lookup_ioc_type_name(ioc_type_name=ioc_type)

            if not ioct_r:
                return ClientApiError(msg=f"IOC type {ioc_type} is invalid", error=ioct_r)

            ioc_type = ioct_r

        if ioc_tags and not isinstance(ioc_tags, list):
            return ClientApiError(f"IOC tags must be a list of str")

        body = {
            "ioc_value": value if value else ioc.get('ioc_value'),
            "ioc_tlp_id": ioc_tlp if ioc_tlp else int(ioc.get('ioc_tlp_id')),
            "ioc_type_id": ioc_type if ioc_type else int(ioc.get('ioc_type_id')),
            "ioc_description": description if description else ioc.get('ioc_description'),
            "ioc_tags": ",".join(ioc_tags) if ioc_tags else ioc.get('ioc_tags'),
            "cid": cid
        }

        return self._s.pi_post(f'case/ioc/update/{ioc_id}', data=body)

    def delete_ioc(self, ioc_id: int, cid: int = None) -> ApiResponse:
        """
        Deletes an IOC from its ID. CID must match the case in which the ioc is stored.

        :param ioc_id: ID of the ioc
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/ioc/delete/{ioc_id}', cid=cid)

    def get_event(self, event_id: int, cid: int = None) -> ApiResponse:
        """
        Returns an event from the timeline

        :param event_id: ID of the event to fetch
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/timeline/events/{event_id}', cid=cid)

    def list_events(self, filter_by_asset: int = 0, cid: int = None) -> ApiResponse:
        """
        Returns a list of events from the timeline. filter_by_asset can be used to return only the events
        linked to a specific asset. In case the asset doesn't exist, an empty timeline is returned.

        :param filter_by_asset: Select the timeline of a specific asset by setting an existing asset ID
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/timeline/events/list/filter/{filter_by_asset}', cid=cid)

    def add_event(self, title:str, date_time: datetime, content: str = None, raw_content: str = None,
                  source: str = None, linked_assets: list = None, category: Union[int, str] = None, tags: list = None,
                  color: str = None, display_in_graph: bool = None,
                  display_in_summary: bool = None, cid: int = None, timezone_string: str = None) -> ApiResponse:
        """
        Adds a new event to the timeline.

        If it is a string, category is lookup-ed up before the addition request is issued.
        it can be either a name or an ID. For performances prefer an ID as it is used directly in the request
        without prior lookup.

        :param title: Title of the event 
        :param date_time: Datetime of the event, including timezone
        :param content: Content of the event (displayed in timeline on GUI)
        :param raw_content: Raw content of the event (displayed in detailed event on GUI)
        :param source: Source of the event 
        :param linked_assets: List of assets to link with this event 
        :param category: Category of the event (MITRE ATT@CK)
        :param color: Left border of the event in the timeline 
        :param display_in_graph: Set to true to display in graph page - Default to true
        :param display_in_summary: Set to true to display in Summary - Default to false
        :param tags: A list of strings to add as tags
        :param timezone_string: Timezone in format +XX:XX or -XX:XX. If none, +00:00 is used
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        if category and isinstance(category, str):
            cat = EventCategoryHelper(session=self._s)
            evtx_cat_r = cat.lookup_event_category_name(event_category=category)

            if not evtx_cat_r:
                return ClientApiError(msg=f"Event category {category} is invalid")

            category = evtx_cat_r

        if not isinstance(date_time, datetime.datetime):
            return ClientApiError(msg=f"Expected datetime object for date_time but got {type(date_time)}")

        if tags and not isinstance(tags, list):
            return ClientApiError(msg=f"Expected list object for tags but got {type(tags)}")

        body = {
            "event_title": title,
            "event_in_graph": display_in_graph if display_in_graph is not None else True,
            "event_in_summary": display_in_summary if display_in_summary is not None else False,
            "event_content": content if content else "",
            "event_raw": raw_content if raw_content else "",
            "event_source": source if source else "",
            "event_assets": linked_assets if linked_assets else [],
            "event_category_id": category if category else "1",
            "event_color": color if color else "",
            "event_date": date_time.strftime('%Y-%m-%dT%H:%M:%S.%f'),
            "event_tags": ','.join(tags) if tags else '',
            "event_tz": timezone_string if timezone_string else "+00:00",
            "cid": cid
        }

        return self._s.pi_post(f'case/timeline/events/add', data=body)

    def update_event(self, event_id: int, title: str=None, date_time: datetime = None, content: str = None,
                     raw_content: str = None, source: str = None, linked_assets: list = None,
                     category: Union[int, str] = None, tags: list = None,
                     color: str = None, display_in_graph: bool = None,
                     display_in_summary: bool = None, cid: int = None, timezone_string: str = None) -> ApiResponse:
        """
        Updates an event of the timeline. event_id needs to be an existing event in the target case.

        If it is a string, category is lookup-ed up before the addition request is issued.
        it can be either a name or an ID. For performances prefer an ID as it is used directly in the request
        without prior lookup.

        :param event_id: Event ID to update
        :param title: Title of the event
        :param date_time: Datetime of the event, including timezone
        :param content: Content of the event (displayed in timeline on GUI)
        :param raw_content: Raw content of the event (displayed in detailed event on GUI)
        :param source: Source of the event
        :param linked_assets: List of assets to link with this event
        :param category: Category of the event (MITRE ATT@CK)
        :param color: Left border of the event in the timeline
        :param display_in_graph: Set to true to display in graph page - Default to true
        :param display_in_summary: Set to true to display in Summary - Default to false
        :param tags: A list of strings to add as tags
        :param timezone_string: Timezone in format +XX:XX or -XX:XX. If none, +00:00 is used
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        event_req = self.get_event(event_id, cid=cid)
        if event_req.is_error():
            return ClientApiError(msg=event_req.get_msg())

        event = event_req.get_data()

        if category and isinstance(category, str):
            cat = EventCategoryHelper(session=self._s)
            evtx_cat_r = cat.lookup_event_category_name(event_category=category)

            if not evtx_cat_r:
                return ClientApiError(msg=f"Event category {category} is invalid")

            category = evtx_cat_r

        if date_time and not isinstance(date_time, datetime.datetime):
            return ClientApiError(msg=f"Expected datetime object for date_time but got {type(date_time)}")

        if tags and not isinstance(tags, list):
            return ClientApiError(msg=f"Expected list object for tags but got {type(tags)}")

        body = {
            "event_title": title if title else event.get('event_title'),
            "event_in_graph": display_in_graph if display_in_graph is not None else event.get('event_in_graph'),
            "event_in_summary": display_in_summary if display_in_summary is not None else event.get('event_in_summary'),
            "event_content": content if content else event.get('event_content'),
            "event_raw": raw_content if raw_content else event.get('event_raw'),
            "event_source": source if source else event.get('event_source'),
            "event_assets": linked_assets if linked_assets else [],
            "event_category_id": category if category else event.get('event_category_id'),
            "event_color": color if color else event.get('event_color'),
            "event_date": date_time.strftime('%Y-%m-%dT%H:%M:%S.%f') if date_time else event.get('event_date'),
            "event_tags": ','.join(tags) if tags else event.get('event_tags'),
            "event_tz": timezone_string if timezone_string else event.get('event_tz'),
            "cid": cid
        }

        return self._s.pi_post(f'case/timeline/events/update/{event_id}', data=body)

    def delete_event(self, event_id: int, cid: int = None) -> ApiResponse:
        """
        Deletes an event from its ID. CID must match the case in which the event is stored

        :param event_id: Event to delete
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/timeline/events/delete/{event_id}', cid=cid)

    def list_tasks(self, cid: int = None) -> ApiResponse:
        """
        Returns a list of tasks linked to the provided case.

        :param cid: Case ID
        :return: ApiResponse object
        """
        return self._s.pi_get(f'case/tasks/list', cid=cid)

    def get_task(self, task_id: int, cid: int = None) -> ApiResponse:
        """
        Returns a task from its ID. task_id needs to be a valid task in the target case.

        :param task_id: Task ID to lookup
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/tasks/{task_id}', cid=cid)

    def add_task(self, title: str, status: Union[str, int], assignee: Union[str, int], description: str = None,
                 tags: list = None, cid: int = None) -> ApiResponse:
        """
        Adds a new task to the target case.

        If they are strings, status and assignee are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.

        :param title: Title of the task
        :param description: Description of the task
        :param assignee: Assignee ID or username
        :param cid: Case ID
        :param tags: Tags of the task
        :param status: String or status ID, need to be a valid status
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        if isinstance(assignee, str):
            user = User(self._s)
            assignee_r = user.lookup_username(username=assignee)
            if assignee_r.is_error():
                return assignee_r

            assignee = assignee_r.get_data().get('user_id')
            if not assignee:
                return ClientApiError(msg=f'Error while looking up username {assignee}')

        elif not isinstance(assignee, int):
            return ClientApiError(msg=f'Invalid assignee type {type(assignee)}')

        if isinstance(status, str):
            tsh = TaskStatusHelper(self._s)
            tsh_r = tsh.lookup_task_status_name(task_status_name=status)
            if tsh_r is None:
                return ClientApiError(msg=f'Invalid task status {status}')
            status = tsh_r

        body = {
            "task_assignee_id": assignee,
            "task_description": description if description else "",
            "task_status_id": status,
            "task_tags": ','.join(tags) if tags else "",
            "task_title":  title,
            "cid": cid
        }

        return self._s.pi_post(f'case/tasks/add', data=body)

    def update_task(self, task_id: int, title: str = None, status: Union[str, int] = None,
                    assignee: Union[int, str] = None, description: str = None,
                    tags: list = None, cid: int = None) -> ApiResponse:
        """
        Updates a task. task_id needs to be a valid task in the target case.

        If they are strings, status and assignee are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.

        :param task_id: ID of the task to update
        :param title: Title of the task
        :param description: Description of the task
        :param assignee: Assignee ID or assignee username
        :param cid: Case ID
        :param tags: Tags of the task
        :param status: String status, need to be a valid status
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        task_req = self.get_task(task_id=task_id)

        if task_req.is_error():
            return ClientApiError(msg=f'Unable to fetch task #{task_id} for update', error=task_req.get_msg())

        if assignee and isinstance(assignee, str):
            user = User(self._s)
            assignee_r = user.lookup_username(username=assignee)
            if assignee_r.is_error():
                return assignee_r

            assignee = assignee_r.get_data().get('user_id')
            if not assignee:
                return ClientApiError(msg=f'Error while looking up username {assignee}')

        elif assignee and not isinstance(assignee, int):
            return ClientApiError(msg=f'Invalid assignee type {type(assignee)}')

        if status and isinstance(status, str):
            tsh = TaskStatusHelper(self._s)
            tsh_r = tsh.lookup_task_status_name(task_status_name=status)
            if tsh_r is None:
                return ClientApiError(msg=f'Invalid task status {status}')
            status = tsh_r

        task = task_req.get_data()

        body = {
            "task_assignee_id": assignee if assignee else task.get('task_assignee_id'),
            "task_description": description if description else task.get('task_description'),
            "task_status_id": status if status else task.get('task_status_id'),
            "task_tags": ",".join(tags) if tags else task.get('task_tags'),
            "task_title":  title if title else task.get('task_title'),
            "cid": cid
        }

        return self._s.pi_post(f'case/tasks/update/{task_id}', data=body)

    def delete_task(self, task_id: int, cid: int = None) -> ApiResponse:
        """
        Deletes a task from its ID. CID must match the case in which the task is stored.

        :param task_id: Task to delete
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/tasks/delete/{task_id}', cid=cid)

    def list_evidences(self, cid: int = None) -> ApiResponse:
        """
        Returns a list of evidences.

        :param cid: Case ID
        :return: ApiResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/evidences/list', cid=cid)

    def get_evidence(self, evidence_id: int, cid: int = None) -> ApiResponse:
        """
        Returns an evidence from its ID. evidence_id needs to be an existing evidence in the target case.

        :param evidence_id: Evidence ID to lookup
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/evidences/{evidence_id}', cid=cid)

    def add_evidence(self, filename: str, file_size: int, description: str = None,
                     file_hash: str = None, cid: int = None) -> ApiResponse:
        """
        Adds a new evidence to the target case.

        :param filename: name of the evidence
        :param file_size: Size of the file
        :param description: Description of the evidence
        :param file_hash: hash of the evidence
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        body = {
            "filename": filename,
            "file_size": file_size,
            "file_description": description,
            "file_hash": file_hash,
            "cid": cid
        }

        return self._s.pi_post(f'case/evidences/add', data=body)

    def update_evidence(self, evidence_id: int, filename: str = None, file_size: int = None, description: str = None,
                        file_hash: str = None, cid: int = None) -> ApiResponse:
        """
        Updates an evidence of the matching case. evidence_id needs to be an existing evidence in the target case.

        :param evidence_id: ID of the evidence
        :param filename: name of the evidence
        :param file_size: Size of the file
        :param description: Description of the evidence
        :param file_hash: hash of the evidence
        :param cid: Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        evidence_req = self.get_evidence(evidence_id=evidence_id, cid=cid)
        if evidence_req.is_error():
            return ClientApiError(msg=f'Unable to fetch evidence #{evidence_id} for update',
                                  error=evidence_req.get_msg())

        evidence = evidence_req.get_data()

        body = {
            "filename": filename if filename else evidence.get('filename'),
            "file_size": file_size if file_size else evidence.get('file_size'),
            "file_description": description if description else evidence.get('file_description'),
            "file_hash": file_hash if file_hash else evidence.get('file_hash'),
            "cid": cid
        }

        return self._s.pi_post(f'case/evidences/update/{evidence_id}', data=body)

    def delete_evidence(self, evidence_id: int, cid: int = None):
        """
        Deletes an evidence from its ID. evidence_id needs to be an existing evidence in the target case.

        :param evidence_id: int - Evidence to delete
        :param cid: int - Case ID
        :return: APIResponse object
        """
        cid = self._assert_cid(cid)

        return self._s.pi_get(f'case/evidences/delete/{evidence_id}', cid=cid)

    def list_global_tasks(self) -> ApiResponse:
        """
        Return a list of global tasks.

        :return: ApiResponse object
        """
        return self._s.pi_get(f'global/tasks/list', cid=1)

    def get_global_task(self, task_id: int) -> ApiResponse:
        """
        Returns a global task from its ID.

        :param task_id: Task ID to lookup
        :return: APIResponse object
        """

        return self._s.pi_get(f'global/tasks/{task_id}', cid=1)

    def add_global_task(self, title: str, status: Union[str, int], assignee: Union[str, int], description: str = None,
                 tags: list = None) -> ApiResponse:
        """
        Adds a new task.

        If they are strings, status and assignee are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.

        :param title: Title of the task
        :param description: Description of the task
        :param assignee: Assignee ID or username
        :param tags: Tags of the task
        :param status: String or status ID, need to be a valid status
        :return: APIResponse object
        """

        if isinstance(assignee, str):
            user = User(self._s)
            assignee_r = user.lookup_username(username=assignee)
            if assignee_r.is_error():
                return assignee_r

            assignee = assignee_r.get_data().get('user_id')
            if not assignee:
                return ClientApiError(msg=f'Error while looking up username {assignee}')

        elif not isinstance(assignee, int):
            return ClientApiError(msg=f'Invalid assignee type {type(assignee)}')

        if status and isinstance(status, str):
            tsh = TaskStatusHelper(self._s)
            tsh_r = tsh.lookup_task_status_name(task_status_name=status)
            if tsh_r is None:
                return ClientApiError(msg=f'Invalid task status {status}')
            status = tsh_r

        body = {
            "task_assignee_id": assignee,
            "task_description": description if description else "",
            "task_status_id": status,
            "task_tags": ','.join(tags) if tags else "",
            "task_title":  title,
            "cid": 1
        }

        return self._s.pi_post(f'global/tasks/add', data=body)

    def update_global_task(self, task_id: int, title: str = None, status: Union[str, int] = None,
                    assignee: Union[int, str] = None, description: str = None,
                    tags: list = None) -> ApiResponse:
        """
        Updates a task. task_id needs to be an existing task in the database.

        If they are strings, status and assignee are lookup-ed up before the addition request is issued.
        Both can be either a name or an ID. For performances prefer an ID as they're used directly in the request
        without prior lookup.

        :param task_id: ID of the task to update
        :param title: Title of the task
        :param description: Description of the task
        :param assignee: Assignee ID or assignee username
        :param tags: Tags of the task
        :param status: String status, need to be a valid status
        :return: APIResponse object
        """

        task_req = self.get_global_task(task_id=task_id)

        if task_req.is_error():
            return ClientApiError(msg=f'Unable to fetch task #{task_id} for update', error=task_req.get_msg())

        if assignee and isinstance(assignee, str):
            user = User(self._s)
            assignee_r = user.lookup_username(username=assignee)
            if assignee_r.is_error():
                return assignee_r

            assignee = assignee_r.get_data().get('user_id')
            if not assignee:
                return ClientApiError(msg=f'Error while looking up username {assignee}')

        elif assignee and not isinstance(assignee, int):
            return ClientApiError(msg=f'Invalid assignee type {type(assignee)}')

        if status and isinstance(status, str):
            tsh = TaskStatusHelper(self._s)
            tsh_r = tsh.lookup_task_status_name(task_status_name=status)
            if tsh_r is None:
                return ClientApiError(msg=f'Invalid task status {status}')
            status = tsh_r

        task = task_req.get_data()

        body = {
            "task_assignee_id": assignee if assignee else task.get('task_assignee_id'),
            "task_description": description if description else task.get('task_description'),
            "task_status_id": status if status else task.get('task_status_id'),
            "task_tags": ",".join(tags) if tags else task.get('task_tags'),
            "task_title":  title if title else task.get('task_title'),
        }

        return self._s.pi_post(f'global/tasks/update/{task_id}', data=body)

    def delete_global_task(self, task_id: int) -> ApiResponse:
        """
        Deletes a global task from its ID. task_id needs to be an existing task in the database.

        :param task_id: int - Task to delete
        :return: APIResponse object
        """

        return self._s.pi_get(f'global/tasks/delete/{task_id}', cid=1)
