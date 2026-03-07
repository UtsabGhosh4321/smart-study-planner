from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import routers
from app.api import auth, tasks, ai


# ======================================
# CREATE FASTAPI APPLICATION
# ======================================
app = FastAPI(
    title="Smart Study Planner API",
    description="AI-powered study planning backend using FastAPI, MongoDB Atlas and OpenAI",
    version="1.0.0"
)


# ======================================
# CORS CONFIGURATION
# ======================================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ⚠ Change this in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ======================================
# ROOT ENDPOINT
# ======================================
@app.get("/", tags=["Health"])
async def root():
    return {
        "message": "Smart Study Planner API is running 🚀",
        "docs": "/docs",
        "status": "success"
    }


# ======================================
# HEALTH CHECK
# ======================================
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "service": "Smart Study Planner API"
    }


# ======================================
# INCLUDE ROUTERS
# ======================================

# Authentication APIs
app.include_router(
    auth.router,
    prefix="/auth",
    tags=["Authentication"]
)

# Task APIs
app.include_router(
    tasks.router,
    prefix="/tasks",
    tags=["Tasks"]
)

# AI Planner APIs
app.include_router(
    ai.router,
    prefix="/ai",
    tags=["AI Planner"]
)