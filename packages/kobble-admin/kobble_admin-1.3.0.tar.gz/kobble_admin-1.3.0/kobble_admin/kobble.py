from dataclasses import dataclass
from kobble_admin.api import HttpClient
from kobble_admin.gateway import KobbleGateway
from kobble_admin.users import KobbleUsers
from kobble_admin.webhooks import KobbleWebhooks


class KobbleOptions:
    def __init__(self, api_base_url="https://sdk.kobble.io"):
        self.api_base_url = api_base_url


@dataclass
class Whoami:
    user_id: str
    project_id: str
    project_slug: str


class Kobble:
    def __init__(self, secret: str, options: KobbleOptions = KobbleOptions()):
        self._secret = secret
        self._http = HttpClient(secret, base_url=options.api_base_url)
        self.gateway = KobbleGateway(http=self._http)
        self.users = KobbleUsers(http=self._http)
        self.webhooks = KobbleWebhooks()

    def whoami(self) -> Whoami:
        payload = self._http.get_json("/auth/whoami")

        return Whoami(
            project_id=payload["projectId"],
            project_slug=payload["projectSlug"],
            user_id=payload["userId"]
        )

    def ping(self) -> bool:
        self._http.get_json("/ping")

        return True
