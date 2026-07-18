from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Field:
    name: str
    label: str
    value: str
    rows: int = 8


@dataclass(frozen=True)
class Product:
    number: int
    slug: str
    name: str
    tagline: str
    accent: str
    fields: tuple[Field, ...]


Analysis = dict[str, Any]

