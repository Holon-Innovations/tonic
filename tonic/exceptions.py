from urllib3 import BaseHTTPResponse


class PopBadResponse(Exception):
    def __init__(self, response: BaseHTTPResponse) -> None:
        self._response = response
        super().__init__(f"{response}: {response.status}")

    @property
    def response(self) -> BaseHTTPResponse:
        return self._response