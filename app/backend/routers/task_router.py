
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
        deadline=todo.deadline
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


@task_router.delete("/api/tasks/{todo_id}", response_class=JSONResponse)
async def delete_task(todo_id: int):
    todo = await Todo.get_by_id(todo_id)
    if not todo:
        raise HTTPException(status_code=404, detail="Задача не найдена!")
    await todo.delete()
    return {"detail": "Задача успешно удалена!"}


@task_router.get("/tasks/category/{todo_id}", response_model=dict)
async def get_category(todo_id: int):
    category = await Todo.get_category_by_id(todo_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Task not found or no category found")
    return {"category": category}
