
from fastapi import FastAPI
from uvicorn import uvicorn

app = FastAPI()

if __name__ == '__main__':
    uvicorn.run('main:app', reload=True, port=8000)