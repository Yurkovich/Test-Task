
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn

from urls.url import url_router
from routers.task_router import task_router
from config.config import db_path


templates = Jinja2Templates(directory="app/frontend/templates")
app = FastAPI()


app.mount("/static", StaticFiles(directory="app/frontend/static"), name="static")
app.include_router(url_router)
app.include_router(task_router)


if __name__ == '__main__':
    from database.database import Database
    db = Database(db_path)
    db.create_table()

    uvicorn.run('main:app', reload=True, port=8000)