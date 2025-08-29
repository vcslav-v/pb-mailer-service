from pydantic import BaseModel
from typing import Type

class EmailEvent(BaseModel):
    email: str


class EmailData(BaseModel):
    subject: str
    short_subject: str
    template_path: str
    schema_model: Type[EmailEvent]
    is_category_block: bool = True
