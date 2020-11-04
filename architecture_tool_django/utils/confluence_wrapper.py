"""
This module is an wrapper of atlassian-python-api as there is API gateway in front of Confluence.
"""
import base64
import re

from atlassian import Confluence
from django.conf import settings

private_auth = {
    "username": settings.CONFLUENCE_USER,
    "password": settings.CONFLUENCE_PASS,
}
extra_headers = {"keyid": settings.API_KEY, "X-Atlassian-Token": "nocheck"}


def tiny_to_page_id(tiny):
    # https://community.atlassian.com/t5/Confluence-questions/What-is-the-algorithm-used-to-create-the-quot-Tiny-links-quot/qaq-p/186555
    return int.from_bytes(
        base64.b64decode(
            tiny.ljust(8, "A").replace("_", "+").replace("-", "/").encode()
        ),
        byteorder="little",
    )


class MyConfluence(Confluence):
    def __init__(self, *args, **kwargs):
        url = settings.CONFLUENCE_URL
        if "url" not in kwargs:
            kwargs["url"] = url
        kwargs.update(private_auth)
        super().__init__(*args, **kwargs)
        self.default_headers.update(extra_headers)

    def request(self, *args, **kwargs):
        # The API is available directly under the gateway address instead of under rest/api
        kwargs["path"] = re.sub(r"^/?rest/api", "", kwargs["path"])
        # The positional/keyword parameter handling in atlassion-python-api is inconsistent
        # (method defined as keyword, but called as positional parameter)
        if len(args) > 0:
            kwargs["method"] = args[0]
        headers = extra_headers.copy()
        if kwargs["headers"]:
            headers.update(kwargs["headers"])
        if not ("method" in kwargs and kwargs["method"] == "PUT"):
            kwargs["headers"] = headers
        return super().request(**kwargs)
