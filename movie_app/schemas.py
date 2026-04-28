from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

class MovieCreate(BaseModel):
    title: str = Field(min_length=10, max_length=128)
    genre: str = Field(min_length=10, max_length=128)
    release_year: int = Field(gt=1900, lt=2100)


class MovieUpdate(BaseModel):
    title: str|None = Field(min_length=10, max_length=128, default=None)
    genre: str|None = Field(min_length=10, max_length=128, default=None)
    release_year: int|None = Field(gt=1900, lt=2100, default=None)


class WatchStatusSet(BaseModel):
    is_watched: bool = Field(default=False)


class MovieRead(BaseModel):
    id: int = Field(gt=0)
    title: str = Field(min_length=10, max_length=128)
    genre: str = Field(min_length=10, max_length=128)
    release_year: int = Field(gt=1900, lt=2100)
    is_watched: bool = Field(default=False)
    created_at: datetime = Field(default=datetime.now)
