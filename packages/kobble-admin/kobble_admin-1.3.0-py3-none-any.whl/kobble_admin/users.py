from datetime import datetime
from typing import Optional, List
from kobble_admin.api import HttpClient
from dataclasses import dataclass
from kobble_admin.products import ProductWithQuota
from kobble_admin.quotas import Quota


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


@dataclass
class QuotaUsage:
    usage: int
    expires_at: str
    limit: int
    is_exceeded: bool


class KobbleUsers:
    def __init__(self, http: HttpClient):
        self._http = http

    def _dict_to_user_active_product(self, d: dict) -> ProductWithQuota:
        return ProductWithQuota(
            id=d["id"],
            name=d["name"],
            quotas=[self._dict_to_quota(q) for q in d["quotas"]]
        )

    def _dict_to_quota(self, d: dict) -> Quota:
        return Quota(
                id=d["id"],
                name=d["name"],
                limit=d["limit"]
        )

    def _dict_to_quota_usage(self, d: dict):
        return QuotaUsage(
            usage=d["usage"],
            is_exceeded=d["isExceeded"],
            limit=d["limit"],
            expires_at=d["expiresAt"]
        )

    def _dict_to_user(self, d: dict) -> User:
        return User(
            id=d["id"],
            email=d["email"],
            name=d["name"],
            verified=d["isVerified"],
            created_at=d["createdAt"]
        )

    def find_by_id(self, id: str) -> User:
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

    def list_active_products(self, id: str) -> List[ProductWithQuota]:
        payload = self._http.get_json(
                "/users/listActiveProducts",
                params={
                    "userId": id,
                }
        )

        return [
            self._dict_to_user_active_product(p) for p in payload["products"]
        ]

    def get_quota_usage(self, id: str, quota_id: str) -> None:
        payload = self._http.get_json(
                "/users/getQuotaUsage",
                params={
                    "userId": id,
                    "quotaId": quota_id,
                }
        )

        return self._dict_to_quota_usage(payload)

    def increment_quota_usage(self, id: str, quota_id: str, increment_by=1) -> None:
        self._http.post_json(
                "/users/incrementQuotaUsage",
                data={
                    "userId": id,
                    "quotaId": quota_id,
                    "incrementBy": increment_by
                }
        )

    def set_quota_usage(self, id: str, quota_id: str, usage: int) -> None:
        self._http.post_json(
                "/users/setQuotaUsage",
                data={
                    "userId": id,
                    "quotaId": quota_id,
                    "usage": usage
                }
        )
