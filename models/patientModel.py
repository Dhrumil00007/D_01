from pydantic import BaseModel
from typing import Optional


class Patient(BaseModel):
    id: Optional[str] = None
    name: str
    age: int
    disease: str
