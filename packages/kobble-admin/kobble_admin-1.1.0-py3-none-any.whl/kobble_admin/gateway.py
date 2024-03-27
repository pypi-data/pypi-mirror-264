import jwt
from dataclasses import dataclass
from typing import Optional, List
from kobble_admin.api import HttpClient

gateway_issuer = "gateway.kobble.io"


@dataclass
class PublicKeyInfo:
    project_id: str
    pem: str


@dataclass
class TokenPayloadQuota:
    id: str
    limit: int
    name: str
    used: int


@dataclass
class TokenPayloadProduct:
    id: str
    quotas: List[TokenPayloadQuota]


@dataclass
class TokenPayloadUser:
    id: str
    email: Optional[str]
    name: Optional[str]
    products: List[TokenPayloadProduct]


@dataclass
class TokenPayload:
    project_id: str
    user: TokenPayloadUser


class KobbleGateway:
    def __init__(self, http: HttpClient):
        self._http = http

    def _fetch_key_info(self) -> PublicKeyInfo:
        res = self._http.get_json("/gateway/getPublicKey")

        return PublicKeyInfo(project_id=res["projectId"], pem=res["pem"])

    def _dict_to_quota(self, quota: dict) -> TokenPayloadQuota:
        return TokenPayloadQuota(
            id=quota["id"],
            used=quota["used"],
            name=quota["name"],
            limit=quota["limit"]
        )

    def _dict_to_product(self, product: dict) -> TokenPayloadProduct:
        return TokenPayloadProduct(
            id=product["id"],
            quotas=[self._dict_to_quota(q) for q in product['quotas']]
        )

    def get_public_key(self) -> str:
        self._fetch_key_info().pem

    def parse_token(
            self,
            token_string: str,
            verify_exp=True,
            verify_aud=True,
            verify_signature=True,
            verify_iss=True
    ) -> TokenPayload:
        key_info = self._fetch_key_info()
        claims = jwt.decode(
            jwt=token_string,
            key=key_info.pem,
            algorithms=["ES256"],
            verify=True,
            audience=key_info.project_id,
            issuer=gateway_issuer,
            options={
                "require": ["exp", "iat", "aud", "iss", "sub", "user"],
                "verify_exp": verify_exp,
                "verify_aud": verify_aud,
                "verify_iss": verify_iss,
                "verify_signature": verify_signature
            }
        )
        payload = TokenPayload(
            project_id=claims['aud'],
            user=TokenPayloadUser(
                id=claims['user']['id'],
                email=claims['user']['email'],
                name=claims['user']['name'],
                products=[
                   self._dict_to_product(p) for p in claims["user"]["products"]
                ]
            )
        )

        return payload
