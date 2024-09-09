
from datetime import datetime
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from database.todo import Todo
from models.task_model import TodoCreate, TodoUpdate


task_router = APIRouter(tags=['Tasks'])


@task_router.get("/api/tasks", response_model=list)
async def get_tasks():
    todos = await Todo.get_all()
    return [todo.__dict__ for todo in todos]


@task_router.get("/api/tasks/{todo_id}", response_model=dict)
async def get_task(todo_id: int):
    todo = await Todo.get_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Задача не найдена!")
    return todo.__dict__


@task_router.post("/api/tasks", response_model=dict)
async def create_task(todo: TodoCreate):
    new_todo = Todo(
        title=todo.title,
        description=todo.description,
        category=todo.category,
        deadline=todo.deadline,
        priority=todo.priority,
        author=todo.author
    )
    await new_todo.create()
    return {"id": new_todo.id}


@task_router.put("/api/tasks/{todo_id}", response_model=dict)
async def update_task(todo_id: int, todo: TodoUpdate):
    existing_todo = await Todo.get_by_id(todo_id)
    if not existing_todo:
        raise HTTPException(status_code=404, detail="Задача не найдена!")

    existing_todo.title = todo.title
    existing_todo.description = todo.description
    existing_todo.category = todo.category
    existing_todo.completed = todo.completed
    existing_todo.date_completed = todo.date_completed
    existing_todo.deadline = todo.deadline
    await existing_todo.update()
    return existing_todo.__dict__


@task_router.patch("/api/tasks/{task_id}/complete")
async def mark_task_completed(task_id: int):
    task = await Todo.get_by_id(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")
    
    if task.completed:
        raise HTTPException(status_code=400, detail="Задача уже завершена")

    task.completed = True
    task.date_completed = datetime.now()
    await task.update()
    
    return task


@task_router.delete("/api/tasks/{todo_id}", response_class=JSONResponse)
async def delete_task(todo_id: int):
    todo = await Todo.get_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Задача не найдена!")
    await todo.delete()
    return {"detail": "Задача успешно удалена!"}
