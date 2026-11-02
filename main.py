
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import create_table
from routers.tasks import router as tasks_router


# Create the database table when the application starts
@asynccontextmanager
async def lifespan(app: FastAPI):
    create_table()
    yield


# Create the FastAPI application
app = FastAPI(
    title="Task Management API",
    lifespan=lifespan
)


# Register the task endpoints
app.include_router(tasks_router)


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Task Management API is working!"
    }


# Health check endpoint
@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }
