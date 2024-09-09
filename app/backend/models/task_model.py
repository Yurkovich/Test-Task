
from pydantic import BaseModel
from datetime import datetime


class Task(BaseModel):
    title: str
    description: str
    category: str
    deadline: datetime
    completed: bool = False
    date_completed: datetime = None
    priority: int
    author: str


class TodoCreate(BaseModel):
    title: str
    description: str
    category: str
    deadline: datetime
    priority: int
    author: str


class TodoUpdate(BaseModel):
    title: str
    description: str
    category: str
    completed: bool
    date_completed: datetime = None
    deadline: datetime
    priority: int