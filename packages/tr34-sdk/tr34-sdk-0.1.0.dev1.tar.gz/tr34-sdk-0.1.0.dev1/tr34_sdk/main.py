import json
import logging
import typing

import aiohttp

from .types import Post
from .exceptions import NoApiKey, NoAdminAccessDisabled, ResponseError

class TR34Api:
    def __init__(self, key: str = None):
        """

        :param key: Api key
        :type key: str
        """

        self.key = key
        self.url = "https://api.top-rule34.com"

    async def get_post(self, post_id: int,
                       raw: bool = False, admin: bool = False) -> typing.Optional[typing.Union[Post, dict]]:
        if raw and not admin:
            raise NoAdminAccessDisabled("raw")
        if (raw or admin) and self.key is None:
            raise NoApiKey("admin")

        headers = {"api-key": self.key} if raw or admin else {}

        async with aiohttp.ClientSession(headers=headers) as s:
            async with s.get(url=self.url + "/getPost", params={"post_id": post_id,
                                                                "raw": json.dumps(raw),
                                                                "admin": json.dumps(admin)}) as r:
                try:
                    response = await r.json()
                except Exception as e:
                    logging.error(f"Error while getting post {e}")
                    return

                if r.status != 200:
                    raise ResponseError(r.status)

        return response if raw else Post(**response)

    async def search_posts(self, tags: list[str] = [],
                           limit: int = 100, page = 0) -> typing.Optional[list[Post]]:
        headers = {"api-key": self.key} if self.key is not None else {}

        async with aiohttp.ClientSession(headers=headers) as s:
            async with s.get(url=self.url + "/getPosts", params={"tags": tags,
                                                                "limit": limit,
                                                                "page": page}) as r:
                try:
                    response = await r.json()
                except Exception as e:
                    logging.error(f"Error while getting post {e}")
                    return

                if r.status != 200:
                    raise ResponseError(r.status)

        return list(map(lambda d: Post(**d), response['posts']))





