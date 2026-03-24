from pydantic import BaseModel

class CreatePost(BaseModel):
    title: str
    content: str

class UpdatePost(BaseModel):
    title: str
    content: str