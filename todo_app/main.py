import uvicorn
from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from database import Base, engine
from router.todo import router as todo_router
import model


BASE_DIR = Path(__file__).resolve().parent

Base.metadata.create_all(bind=engine)

app = FastAPI()

# 정적 파일 연결
app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR / "static"),
    name="static",
)

# Todo 라우터 등록
app.include_router(todo_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
