from dataclasses import dataclass
from kobble_admin.quotas import Quota

@dataclass
class Product:
    id: str
    name: str


@dataclass
class ProductWithQuota:
    id: str
    name: str
    quotas: list[Quota]
