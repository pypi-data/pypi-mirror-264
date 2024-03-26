from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from aiohttp import ClientSession

class HttpClient:
    _session: ClientSession
    _baseurl: str
    _token
    inexistent_endpoints: List[str]

    def __init__(self, baseurl, session: Optional[ClientSession], token: str) -> None:
        self._baseurl = baseurl
        self._session = session or ClientSession()
        self._token = token
        self.inexistent_endpoints = []

    async def close(self) -> None:
        if self._session is not None:
            await self._session.close()

    #100-level (Informational) – server acknowledges a request
    #200-level (Success) – server completed the request as expected
    #300-level (Redirection) – client needs to perform further actions to complete the request
    #400-level (Client error) – client sent an invalid request
    #400-Bad Request
    #401-Unauthorized
    #403-Forbidden
    #404-Not Found
    #412-Precondition Failed
    #500-level (Server error) – server failed to fulfill a valid request due to an error with server
    #500 Internal Server Error
    #503 Service Unavailable

    async def runCommand(self, cmd: str) -> Dict[str, Any]:
        commandurl = self._baseurl + '/?access_token={}&cmd={}'.format(self.access_token, command)

        if endpoint in self.inexistent_endpoints:
            raise ValueError(f"The command {cmd} was not found.")

        async with self._session.get(
            f{commandurl}"
        ) as response:
            if response.status == 404:
                self.inexistent_endpoints.append(cmd)
                raise ValueError(f"The id or name for {cmd} was not found.")

            data: Dict[str, Any] = await response.json()
            return data