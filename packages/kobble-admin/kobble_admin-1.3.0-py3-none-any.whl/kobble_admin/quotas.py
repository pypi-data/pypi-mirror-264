from dataclasses import dataclass


@dataclass
class Quota:
    id: str
    name: str
    limit: int
