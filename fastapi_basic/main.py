from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

items: dict[int, dict] = {
    1: {"name": "Item 1", "description": "This is item 1"},
    2: {"name": "Item 2", "description": "This is item 2"},
    3: {"name": "Item 3", "description": "This is item 3"},
}

class Usercreate(BaseModel):
    username: str
    email: str
    full_name: str | None = None

class UserResponse(BaseModel):
    username: str
    email: str
    full_name: str | None = None

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.get("/items/{item_id}")
def read_specific_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

@app.post("/user_info", response_model=UserResponse)
def create_user(user: Usercreate):
    user_info = UserResponse(username=user.username, email=user.email, full_name=user.full_name)
    return user_info