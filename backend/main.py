import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from db import init_db
from routes.tasks import router as tasks_router
from routes.chat import router as chat_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the database and create tables (incl. Conversation, Message)
    init_db()
    yield
    # Clean up here if needed

app = FastAPI(lifespan=lifespan)

# Allow all origins for dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router)
app.include_router(chat_router)

@app.get("/")
def read_root():
    return {"message": "Hackathon Todo API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
