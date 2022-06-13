from typing import Union

from fastapi import FastAPI

app = FastAPI()

# TODO: 1). Parse #words 2). Implement jobs 3). Implement UI


@app.get("/")
def read_root():
    return "Index page"


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}