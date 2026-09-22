from fastapi import FastAPI

from .database import engine, Base
from .routers import auth, jobs, interviews, dashboard


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="JobTrack API",
    description="Job Application Management REST API",
    version="1.0.0"
)


app.include_router(auth.router)
app.include_router(jobs.router)
app.include_router(interviews.router)
app.include_router(dashboard.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to JobTrack API",
        "status": "running"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy"
    }


@app.get("/about")
def about():
    return {
        "name": "JobTrack API",
        "description": "Job Application Management REST API",
        "version": "1.0.0"
    }




