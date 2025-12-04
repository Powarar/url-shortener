from pydantic import BaseModel, field_validator, HttpUrl

class Link(BaseModel):
    link: HttpUrl
    