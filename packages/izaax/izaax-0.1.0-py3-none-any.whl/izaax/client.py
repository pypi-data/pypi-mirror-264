from __future__ import annotations

import html
import os
from pathlib import Path
from urllib.parse import urljoin

import feedparser
import httpx

from .item import RSSItem

BASE_URL = "http://www.izaax.net"


class IzaaxClient:
    def __init__(self, username: str, password: str, output_dir: str | Path = "outputs") -> None:
        self.username = username
        self.password = password
        self.output_dir = Path(output_dir)
        self.client = httpx.Client()

    @classmethod
    def from_env(cls) -> IzaaxClient:
        username = os.getenv("IZAAX_USERNAME")
        if username is None:
            raise ValueError("IZAAX_USERNAME is not set")

        password = os.getenv("IZAAX_PASSWORD")
        if password is None:
            raise ValueError("IZAAX_PASSWORD is not set")

        output_dir = os.getenv("IZAAX_OUTPUT_DIR")
        if output_dir is None:
            output_dir = "outputs"

        return cls(username=username, password=password, output_dir=output_dir)

    def save_text(self, text: str, filename: str) -> None:
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # text = html.unescape(text)

        f = self.output_dir / filename
        with open(f, "w") as fp:
            fp.write(text)

    def login(self) -> None:
        url = urljoin(BASE_URL, "/blog/wp-login.php")
        payload = {
            "log": self.username,
            "pwd": self.password,
            "wp-submit": "登入",
            "redirect_to": "http://www.izaax.net/blog/wp-admin/",
            "testcookie": 1,
        }
        resp = self.client.post(url=url, data=payload)
        resp.raise_for_status()

        self.save_text(html.unescape(resp.text), "login.html")

    def blog(self) -> httpx.Response:
        url = urljoin(BASE_URL, "/blog/")

        resp = self.client.get(url=url)
        resp.raise_for_status()

        self.save_text(resp.text, "blog.html")

        return resp

    def p(self, page_number: int) -> httpx.Response:
        # http://www.izaax.net/blog/?p=11384
        url = urljoin(BASE_URL, "/blog/")
        resp = self.client.get(url, params={"p": page_number})
        resp.raise_for_status()

        self.save_text(resp.text, f"p_{page_number}.html")

        return resp

    def read_rss(self) -> list[RSSItem]:
        url = urljoin(BASE_URL, "/blog/")

        resp = self.client.get(url=url, params={"feed": "rss2"})
        resp.raise_for_status()

        rss = feedparser.parse(resp.text)
        return [RSSItem(title=e.title, description=e.description, link=e.link) for e in rss.entries]
