from pydantic import BaseModel, ConfigDict, Field


class ScoreCreate(BaseModel):
    """????????????"""

    student_id: int = Field(description='??ID')
    exam_order: int = Field(ge=1, description='????')
    score: int = Field(ge=0, le=100, description='??')


class ScoreUpdate(BaseModel):
    """????????????"""

    student_id: int = Field(description='??ID')
    exam_order: int = Field(ge=1, description='????')
    score: int = Field(ge=0, le=100, description='??')


class ScoreDelete(BaseModel):
    """????????????"""

    student_id: int = Field(description='??ID')
    exam_order: int = Field(ge=1, description='????')


class ScoreRead(BaseModel):
    """???????????"""

    id: int
    student_id: int
    exam_order: int
    score: int
    status: int

    model_config = ConfigDict(from_attributes=True)
