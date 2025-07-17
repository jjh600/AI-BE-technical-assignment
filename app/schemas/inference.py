from pydantic import BaseModel
from typing import List, Optional


class PositionDate(BaseModel):
    year: int
    month: Optional[int] = None


class StartEndDate(BaseModel):
    start: PositionDate
    end: Optional[PositionDate] = None


class Position(BaseModel):
    title: str
    companyName: str
    description: Optional[str] = None
    startEndDate: StartEndDate
    companyLocation: Optional[str] = None
    companyLogo: Optional[str] = None


class EducationDateRange(BaseModel):
    startDateOn: dict
    endDateOn: Optional[dict] = None


class Education(BaseModel):
    grade: Optional[str] = None
    degreeName: Optional[str] = None
    schoolName: Optional[str] = None
    description: Optional[str] = None
    fieldOfStudy: Optional[str] = None
    startEndDate: Optional[str] = None
    originStartEndDate: Optional[EducationDateRange] = None


class ExperienceInferenceInput(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    headline: Optional[str] = None
    summary: Optional[str] = None
    linkedinUrl: Optional[str] = None
    photoUrl: Optional[str] = None
    industryName: Optional[str] = None
    skills: Optional[List[str]] = None
    website: Optional[List[str]] = None
    projects: Optional[List[str]] = None
    recommendations: Optional[List[str]] = None
    positions: List[Position]
    educations: Optional[List[Education]] = None


class ExperienceInferenceOutput(BaseModel):
    experiences: List[str]
