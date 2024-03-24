from __future__ import annotations

from urllib.parse import parse_qs
from urllib.parse import urlparse

from pydantic import BaseModel


class RSSItem(BaseModel):
    title: str
    description: str
    link: str

    @property
    def page_id(self) -> str:
        parsed = urlparse(self.link)
        qs = parse_qs(parsed.query)

        p = qs.get("p")
        if not p:
            raise ValueError("p not found")

        return p[0]

    @property
    def redis_key(self) -> str:
        return f"izaax:blog:p:{self.page_id}"
