from datetime import datetime
from typing import Optional
from kobble_admin.api import HttpClient
from dataclasses import dataclass


@dataclass
class User:
    id: str
    email: str
    name: Optional[str]
    created_at: datetime
    verified: bool


@dataclass
class PaginatedUserList:
    page: int
    count: int
    data: list[User]
    total: int
    has_next: bool


class KobbleUsers:
    def __init__(self, http: HttpClient):
        self._http = http

    def _dict_to_user(self, d: dict) -> User:
        return User(
            id=d["id"],
            email=d["email"],
            name=d["name"],
            verified=d["isVerified"],
            created_at=d["createdAt"]
        )

    def find_unique(self, id: str) -> User:
        payload = self._http.get_json(
            "/users/findById",
            params={"userId": id}
        )

        return self._dict_to_user(payload)

    def list(self, limit=50, page=1):
        payload = self._http.get_json(
            "/users/list",
            params={
                "limit": limit,
                "page": page,
            }
        )

        return PaginatedUserList(
            page=payload['page'],
            count=payload['count'],
            data=[self._dict_to_user(u) for u in payload['data']],
            total=payload['total'],
            has_next=payload['hasNext']
        )
