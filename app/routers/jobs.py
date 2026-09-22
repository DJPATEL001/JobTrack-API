from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import (
    JobCreate,
    JobResponse,
    JobStatus,
    JobStatusUpdate,
    JobUpdate,
)


router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"]
)

@router.post("", status_code=201, response_model=JobResponse)
def create_job(
    job: JobCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):
 
    new_job = models.Job(
        user_id=current_user.id,
        company_name=job.company_name,
        job_title=job.job_title,
        location=job.location,
        job_type=job.job_type,
        salary=job.salary,
        application_date=job.application_date,
        status=job.status,
        job_url=job.job_url,
        company_website=job.company_website,
        description=job.description,
        remote=job.remote
    )

    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    return new_job

@router.get("", response_model=list[JobResponse])
def get_jobs(
    status: JobStatus | None = None,
    company: str | None = None,
    search: str | None = None,
    from_date: date | None = None,
    to_date: date | None = None,
    sort_by: str = "id",
    sort_order: str = Query("asc", pattern="^(asc|desc)$"),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)):

    query = db.query(models.Job).filter(
        models.Job.user_id == current_user.id
    )

    if status:
        query = query.filter(
            models.Job.status == status.value
        )

    if company:
        query = query.filter(
            models.Job.company_name.ilike(f"%{company}%")
        )

    if search:
        query = query.filter(
            models.Job.job_title.ilike(f"%{search}%")
        )

    if from_date:
        query = query.filter(
        models.Job.application_date >= from_date
        )

    if to_date:
        query = query.filter(
            models.Job.application_date <= to_date
        )

    sort_column = getattr(models.Job, sort_by, None)

    if sort_column is None:
        raise HTTPException(
            status_code=400,
            detail="Invalid sort field"
        )

    if sort_order.lower() == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    jobs = query.offset(skip).limit(limit).all()

    return jobs


@router.get("/{job_id}", response_model=JobResponse)
def get_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    job = db.query(models.Job).filter(
        models.Job.id == job_id,
        models.Job.user_id == current_user.id
    ).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job

@router.patch("/{job_id}/status", response_model=JobResponse)
def update_job_status(
    job_id: int,
    status_data: JobStatusUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    job = db.query(models.Job).filter(
        models.Job.id == job_id,
        models.Job.user_id == current_user.id
    ).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    job.status = status_data.status.value

    db.commit()
    db.refresh(job)

    return job




@router.put("/{job_id}", response_model=JobResponse)
def update_job(
    job_id: int,
    job_data: JobUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    job = db.query(models.Job).filter(
    models.Job.id == job_id,
    models.Job.user_id == current_user.id
).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    update_data = job_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(job, key, value)

    db.commit()
    db.refresh(job)

    return job

@router.delete("/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    job = db.query(models.Job).filter(
        models.Job.id == job_id,
        models.Job.user_id == current_user.id
    ).first()

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    db.delete(job)
    db.commit()

    return {
        "message": "Job deleted successfully"
    }