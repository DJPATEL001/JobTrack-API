from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base


class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    company_name = Column(String(100), nullable=False)
    job_title = Column(String(100), nullable=False)
    location = Column(String(100))
    job_type = Column(String(50))
    salary = Column(String(50))
    application_date = Column(Date)
    status = Column(String(50), default="Applied")
    job_url = Column(String(500))
    company_website = Column(String(500))
    description = Column(String(1000))
    remote = Column(String(20))

    owner = relationship(
        "User",
        back_populates="jobs"
    )
    
    interviews = relationship(
    "Interview",
    back_populates="job",
    cascade="all, delete-orphan"
    )


class Interview(Base):
    __tablename__ = "interviews"

    id = Column(Integer, primary_key=True, index=True)

    job_id = Column(
        Integer,
        ForeignKey("jobs.id"),
        nullable=False
    )

    interview_date = Column(Date, nullable=False)
    round = Column(String(50), nullable=False)
    interviewer = Column(String(100))
    mode = Column(String(30))
    result = Column(String(50))
    notes = Column(String(1000))

    job = relationship(
        "Job",
        back_populates="interviews"
    )


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    hashed_password = Column(String(255), nullable=False)

    jobs = relationship(
        "Job",
        back_populates="owner",
        cascade="all, delete-orphan"
    )