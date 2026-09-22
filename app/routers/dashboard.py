from fastapi import APIRouter, Depends
from sqlalchemy import case, func
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
from app.dependencies import get_current_user
from app.schemas import DashboardStats

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"]
)

@router.get("/stats", response_model=DashboardStats)
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    stats = db.query(
        func.count(models.Job.id).label("total_jobs"),

        func.sum(
            case(
                (models.Job.status == "Applied", 1),
                else_=0
            )
        ).label("applied"),

        func.sum(
            case(
                (models.Job.status == "Shortlisted", 1),
                else_=0
            )
        ).label("shortlisted"),

        func.sum(
            case(
                (models.Job.status == "Assessment", 1),
                else_=0
            )
        ).label("assessment"),

        func.sum(
            case(
                (models.Job.status == "Interview", 1),
                else_=0
            )
        ).label("interview"),

        func.sum(
            case(
                (models.Job.status == "Selected", 1),
                else_=0
            )
        ).label("selected"),

        func.sum(
            case(
                (models.Job.status == "Rejected", 1),
                else_=0
            )
        ).label("rejected"),

        func.sum(
            case(
                (models.Job.status == "Withdrawn", 1),
                else_=0
            )
        ).label("withdrawn")
    ).filter(
        models.Job.user_id == current_user.id
    ).first()

    total_interviews = db.query(
        func.count(models.Interview.id)
    ).join(
        models.Job
    ).filter(
        models.Job.user_id == current_user.id
    ).scalar()

    return {
        "total_jobs": stats.total_jobs or 0,
        "applied": stats.applied or 0,
        "shortlisted": stats.shortlisted or 0,
        "assessment": stats.assessment or 0,
        "interview": stats.interview or 0,
        "selected": stats.selected or 0,
        "rejected": stats.rejected or 0,
        "withdrawn": stats.withdrawn or 0,
        "total_interviews": total_interviews or 0
    }