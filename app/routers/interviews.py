from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import (
    InterviewCreate,
    InterviewResponse,
    InterviewUpdate,
)

router = APIRouter(
    tags=["Interviews"]
)


@router.post(
    "/jobs/{job_id}/interviews", status_code=201,
    response_model=InterviewResponse
)
def create_interview(
    job_id: int,
    interview: InterviewCreate,
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

    new_interview = models.Interview(
        job_id=job.id,
        interview_date=interview.interview_date,
        round=interview.round,
        interviewer=interview.interviewer,
        mode=interview.mode,
        result=interview.result,
        notes=interview.notes
    )

    db.add(new_interview)
    db.commit()
    db.refresh(new_interview)

    return new_interview

@router.get(
    "/jobs/{job_id}/interviews",
    response_model=list[InterviewResponse]
)
def get_interviews(
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

    interviews = db.query(models.Interview).filter(
        models.Interview.job_id == job_id
    ).order_by(
        models.Interview.interview_date.asc()
    ).all()

    return interviews


@router.put(
    "/interviews/{interview_id}",
    response_model=InterviewResponse
)
def update_interview(
    interview_id: int,
    interview_data: InterviewUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    interview = db.query(models.Interview).join(
        models.Job
    ).filter(
        models.Interview.id == interview_id,
        models.Job.user_id == current_user.id
    ).first()

    if interview is None:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    update_data = interview_data.model_dump(
        exclude_unset=True
    )

    for key, value in update_data.items():
        setattr(interview, key, value)

    db.commit()
    db.refresh(interview)

    return interview


@router.delete("/interviews/{interview_id}")
def delete_interview(
    interview_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    interview = db.query(models.Interview).join(
        models.Job
    ).filter(
        models.Interview.id == interview_id,
        models.Job.user_id == current_user.id
    ).first()

    if interview is None:
        raise HTTPException(
            status_code=404,
            detail="Interview not found"
        )

    db.delete(interview)
    db.commit()

    return {
        "message": "Interview deleted successfully"
    }
