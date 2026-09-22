from datetime import date
from pydantic import BaseModel, ConfigDict
from enum import Enum

class JobStatus(str, Enum):
    APPLIED = "Applied"
    SHORTLISTED = "Shortlisted"
    ASSESSMENT = "Assessment"
    INTERVIEW = "Interview"
    SELECTED = "Selected"
    REJECTED = "Rejected"
    WITHDRAWN = "Withdrawn"

class JobStatusUpdate(BaseModel):
    status: JobStatus


class JobCreate(BaseModel):
    company_name: str
    job_title: str
    location: str | None = None
    job_type: str | None = None
    salary: str | None = None
    application_date: date | None = None
    status: JobStatus = JobStatus.APPLIED
    job_url: str | None = None
    company_website: str | None = None
    description: str | None = None
    remote: str | None = None


class JobResponse(BaseModel):
    id: int
    company_name: str
    job_title: str
    location: str | None = None
    job_type: str | None = None
    salary: str | None = None
    application_date: date | None = None
    status: str
    job_url: str | None = None
    company_website: str | None = None
    description: str | None = None
    remote: str | None = None

    model_config = ConfigDict(from_attributes=True)


class JobUpdate(BaseModel):
    company_name: str | None = None
    job_title: str | None = None
    location: str | None = None
    job_type: str | None = None
    salary: str | None = None
    application_date: date | None = None
    status: JobStatus | None = None
    job_url: str | None = None
    company_website: str | None = None
    description: str | None = None
    remote: str | None = None

class InterviewCreate(BaseModel):
    interview_date: date
    round: str
    interviewer: str | None = None
    mode: str | None = None
    result: str | None = None
    notes: str | None = None


class InterviewResponse(BaseModel):
    id: int
    job_id: int
    interview_date: date
    round: str
    interviewer: str | None = None
    mode: str | None = None
    result: str | None = None
    notes: str | None = None

    model_config = ConfigDict(from_attributes=True)

class InterviewUpdate(BaseModel):
    interview_date: date | None = None
    round: str | None = None
    interviewer: str | None = None
    mode: str | None = None
    result: str | None = None
    notes: str | None = None


class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class DashboardStats(BaseModel):
    total_jobs: int
    applied: int
    shortlisted: int
    assessment: int
    interview: int
    selected: int
    rejected: int
    withdrawn: int
    total_interviews: int