from pydantic import BaseModel


class Tag(BaseModel):
    id: int
    name: str
    is_artist: bool
    is_character: bool
    count: int
    is_copyright: bool


class SimpleTag(BaseModel):
    name: str
    count: int


class PostTags(BaseModel):
    count: int
    copyright: list[SimpleTag]
    artist: list[SimpleTag]
    character: list[SimpleTag]
    regular: list[SimpleTag]
