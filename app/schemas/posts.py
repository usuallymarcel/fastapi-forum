from typing import Annotated
from pydantic import BaseModel, Field

class Post(BaseModel):
    title: Annotated[str, Field(max_length=200)]
    slug: Annotated[str, Field(max_length=200)]
    content: Annotated[str, Field(max_length=10000)]
    tags: Annotated[str, Field(max_length=300)]

