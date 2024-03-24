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

import logging as logger

import requests
from packaging.version import Version
from requests.packages.urllib3.exceptions import InsecureRequestWarning

from helper.utils import ApiResponse

log = logger.getLogger(__name__)

"""API_VERSION
The API version is not directly correlated with Iris version. 
Server has an endpoint /api/versions which should returns the API compatible versions 
it can handles. 
"""
API_VERSION = "1.0.1"

"""client_session
Defines a global session, accessible by all classes. client_session is of type ClientSession.
"""
client_session = None


class ClientSession(object):
    """
    Represents a client that can interacts with Iris. It is basic wrapper handling authentication and the requests
    to the server.
    """
    def __init__(self, apikey, host=None, agent="iris-client", ssl_verify=True, proxy=None, timeout=120):
        """
        Initialize the ClientSession. APIKey validity is verified as well as API compatibility between the client
        and the server.
        Version verification expects to fall into the following schema :
            `Version(server_min_api_version) <= Version(client_api_version) <= Version(server_max_api_version)`

        If the client does not find itself compatible, an exception is raised.

        Once successfully initialized, the session become available through global var client_session.

        :param apikey: A valid API key. It can be fetched from My profile > API Key
        :param host: Target IRIS server full URL eg https://iris.local:9443
        :param agent: User agent to issue the requests with
        :param ssl_verify: Set or unset SSL verification
        :param proxy: Proxy parameters - For future use only
        :param timeout: Default timeout for requests
        """
        self._apikey = apikey
        self._host = host
        self._agent = agent
        self._ssl_verify = ssl_verify
        self._proxy = proxy
        self._timeout = timeout

        if not self._ssl_verify:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

        self._check_apikey_validity()

        self._check_api_compatibility()

        global client_session
        client_session = self

    def preload_base_objects(self) -> None:
        """
        Preload the base objects most commonly used. This simply init the BaseObjects
        class, which in turns requests and build all the most common objects such as
        AnalysisStatus, EventCategory, EventType, etc.

        For future use only

        :return: None
        """
        pass

    def _check_api_compatibility(self) -> bool:
        """
        Checks that the server and client can work together.
        The methods expects the following :
        `Version(server_min_api_version) <= Version(client_api_version) <= Version(server_max_api_version)`

        If API is not compatible, an exception is raised.

        :raises: Exception if not API compatible
        :return: bool
        """
        resp = self.pi_get('api/versions')
        if resp.is_error():
            raise Exception('Unable to contact endpoint api/versions')

        versions = resp.get_data()
        min_ver = versions.get('api_min')
        max_ver = versions.get('api_current')

        if Version(min_ver) <= Version(API_VERSION) <= Version(max_ver):
            return True

        raise Exception(f'Incompatible API version. Server expects {min_ver} -> {max_ver} but client is {API_VERSION}')

    def _check_apikey_validity(self) -> bool:
        """
        Checks the validity of the provided API key (emptiness, string and authorized).
        If the key is invalid, a ValueError exception is raised.

        :raises: ValueError if the API key is invalid
        :return: bool
        """
        if not isinstance(self._apikey, str):
            raise ValueError('API key must be a string')

        if not self._apikey:
            raise ValueError('API key can not be an empty string')

        resp = self.pi_get('api/ping')
        if resp.is_error():
            raise ValueError('Invalid API key')

        return True

    def _pi_uri(self, uri: str = None):
        """
        Wraps the provided uri around the URL.

        :param uri: URI to request
        :return: Str - URL to request
        """
        return self._host + '/' + uri

    def pi_get(self, uri: str, cid: int = None) -> ApiResponse:
        """
        Adds the CID information needed by the server when issuing GET requests
        and then issue the request itself.

        :param uri: URI endpoint to request
        :param cid: Target case ID
        :return: ApiResponse object
        """
        if cid:
            uri = f"{uri}?cid={cid}"

        return self._pi_request(uri, type='GET')

    def pi_post(self, uri: str, data: dict) -> ApiResponse:
        """
        Issues a POSt request with the provided data. Simple wrapper around _pi_request

        :param uri: URI endpoint to request
        :param data: data to be posted. Expect a dict
        :return: ApiResponse object
        """
        return self._pi_request(uri, type='POST', data=data)

    def _pi_request(self, uri: str, type: str = None, data: dict = None) -> ApiResponse:
        """
        Make a request (GET or POST) and handle the errors. The authentication header is added.

        :raises: Exception if server can't be reached or if server replied 500
        :param uri: URI to request
        :param type: Type of the request [POST or GET]
        :param data: dict to send if request type is POST
        :return: ApiResponse object
        """

        try:

            headers = {
                'Content-Type': "application/json",
                'Authorization': "Bearer " + self._apikey
                }
            if type == "POST":
                log.debug(f'POST : {self._pi_uri(uri)}')
                response = requests.post(url=self._pi_uri(uri),
                                         json=data,
                                         verify=self._ssl_verify,
                                         timeout=self._timeout,
                                         headers=headers)
            elif type == "GET":
                log.debug(f'GET : {self._pi_uri(uri)}')
                response = requests.get(url=self._pi_uri(uri),
                                        verify=self._ssl_verify,
                                        timeout=self._timeout,
                                        headers=headers)

            else:
                return ApiResponse()

        except requests.exceptions.ConnectionError as e:
            raise Exception("Unable to connect to endpoint {host}. Please check URL and ports".format(host=uri))

        if response.status_code == 500:
            log.critical('Server replied 500')
            raise Exception("Server side error. Please check server logs for more information")

        log.debug(f'Server replied with status {response.status_code}')

        return ApiResponse(response.content, uri=uri)

