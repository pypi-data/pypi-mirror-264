from dataclasses import dataclass
from datetime import timedelta
from typing import NamedTuple


class ResultMeta(NamedTuple):
    rows: int
    duration: timedelta


@dataclass
class DbInfo:
    database: str
    host: str
    host_address: str
    port: str
    schema: str
    user: str
