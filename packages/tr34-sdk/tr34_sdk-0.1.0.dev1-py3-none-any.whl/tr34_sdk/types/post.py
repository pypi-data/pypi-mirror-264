import logging
import os.path
import typing

import aiohttp

from pydantic import BaseModel
from datetime import datetime

from .tags import PostTags


class File(BaseModel):
    file: str
    type: str

    async def download(self, path: str = "./downloads"):
        try:
            os.mkdir(path)
        except: pass

        async with aiohttp.ClientSession() as s:
            async with s.get(url=self.file) as r:
                with open(os.path.join(path, os.path.basename(self.file)), "wb") as file:
                    file.write(await r.read())

class Post(BaseModel):
    post_id: int
    tags: list[str]
    save_date: datetime
    url: str

    main: File
    preview: File

    async def get_tags(self) -> typing.Optional[PostTags]:
        async with aiohttp.ClientSession() as s:
            async with s.get(url="https://api.top-rule34.com/getPostTags", params={"id": self.post_id}) as r:
                try:
                    response = await r.json()
                except Exception as e:
                    logging.error(f"Error while getting post {e}")
                    return

        return PostTags(count=response["count"], copyright=response["tags"]['copyright'],
                        artist=response["tags"]['artist'], character=response["tags"]['character'],
                        regular=response["tags"]['regular'])

