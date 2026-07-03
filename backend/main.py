from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from database import init_db
from routes.villages import router as villages_router
from routes.ai_modules import router as ai_router

load_dotenv()

app = FastAPI(
    title="AI Smart Village Development Planner",
    description="AI-powered system for rural development planning in India.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(villages_router)
app.include_router(ai_router)

@app.on_event("startup")
def startup():
    init_db()
    print("Village Planner API is running!")
    print("Docs: http://localhost:8000/docs")

@app.get("/health")
def health():
    return {"status": "ok", "app": "Smart Village Planner"}