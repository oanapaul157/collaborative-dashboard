from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers import boards, columns, tasks

app = FastAPI(title="Collaborative Dashboard API")

# Lets the browser call this API from the Vite dev server (a different origin/port).
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(boards.router)
app.include_router(columns.router)
app.include_router(tasks.router)


@app.get("/health")
def health():
    return {"status": "ok"}

