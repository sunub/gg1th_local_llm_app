from pathlib import Path

from fastapi import APIRouter, Depends, Form, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session

import model
from dependencies import get_db


router = APIRouter(tags=["todo"])

BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=BASE_DIR / "templates")


class TodoUpdate(BaseModel):
    task: str
    completed: bool


@router.get("/edit/{todo_id}")
def edit_page(
    req: Request,
    todo_id: int,
    db: Session = Depends(get_db),
):
    todo = db.query(model.Todo).filter(model.Todo.id == todo_id).first()

    return templates.TemplateResponse(
        request=req,
        name="edit.html",
        context={"todo": todo},
    )


@router.get("/")
def home(
    req: Request,
    db: Session = Depends(get_db),
):
    todos = db.query(model.Todo).all()

    return templates.TemplateResponse(
        request=req,
        name="home.html",
        context={"todos": todos},
    )


@router.patch("/todo/{todo_id}")
def update_task(
    todo_id: int,
    payload: TodoUpdate,
    db: Session = Depends(get_db),
):
    todo = db.query(model.Todo).filter(model.Todo.id == todo_id).first()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    todo.task = payload.task
    todo.completed = payload.completed

    db.commit()

    return {
        "id": todo.id,
        "task": todo.task,
        "completed": todo.completed,
    }


@router.delete(
    "/todo/{todo_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_task(
    todo_id: int,
    db: Session = Depends(get_db),
):
    todo = db.query(model.Todo).filter(model.Todo.id == todo_id).first()

    if todo is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo not found",
        )

    db.delete(todo)
    db.commit()


@router.post("/todo")
def add_task(
    task: str = Form(...),
    db: Session = Depends(get_db),
):
    todo = model.Todo(task=task)

    db.add(todo)
    db.commit()

    return RedirectResponse(
        url=router.url_path_for("home"),
        status_code=status.HTTP_303_SEE_OTHER,
    )
