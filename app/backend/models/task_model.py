
from pydantic import BaseModel
from datetime import datetime


class Task(BaseModel):
    title: str
    description: str
    category: str
    priority: int
    author: str
    deadline: datetime
    completed: bool = False
    date_completed: datetime = None
    

class TodoCreate(BaseModel):
    title: str
    description: str
    category: str
    priority: int
    author: str
    deadline: datetime


class TodoUpdate(BaseModel):
    title: str
    description: str
    category: str
    priority: int
    author: str
    deadline: datetime
    completed: bool
    date_completed: datetime = None