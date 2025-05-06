from fastapi import FastAPI
from pydantic import ValidationError

from songs_api.config import load_config

try:
    config = load_config("config.yml")
except ValidationError as e:
    print(f"A problem occurred while reading the configuration file: {e}")
    exit(1)
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
