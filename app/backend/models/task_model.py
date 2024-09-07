from pydantic import BaseModel
from datetime import datetime

class Todo(BaseModel):
    title: str
    description: str
    category: str
    deadline: datetime
    completed: bool = False
    date_completed: datetime = None