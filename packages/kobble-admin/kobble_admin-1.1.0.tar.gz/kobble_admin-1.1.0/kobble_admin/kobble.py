from dataclasses import dataclass
from kobble_admin.api import HttpClient
from kobble_admin.gateway import KobbleGateway
from kobble_admin.users import KobbleUsers


@dataclass
class KobbleOptions:
    api_base_url = "https://sdk.kobble.io"


@dataclass
class Whoami:
    userId: str
    projectId: str
    projectSlug: str


class Kobble:
    def __init__(self, secret: str, options: KobbleOptions = KobbleOptions()):
        self._secret = secret
        self._http = HttpClient(secret, base_url=options.api_base_url)
        self.gateway = KobbleGateway(http=self._http)
        self.users = KobbleUsers(http=self._http)

    def whoami(self) -> Whoami:
        payload = self._http.get_json("/auth/whoami")

        return Whoami(
            projectId=payload["projectId"],
            projectSlug=payload["projectSlug"],
            userId=payload["userId"]
        )

    def ping(self) -> bool:
        self._http.get_json("/ping")

        return True
