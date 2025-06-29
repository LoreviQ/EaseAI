from datetime import datetime
from typing import List, Optional
from uuid import UUID

from pydantic import BaseModel


class DeliveryTechnique(BaseModel):
    technique: str
    description: str
    when_to_use: Optional[str]
    example: Optional[str]


class PracticeExercise(BaseModel):
    title: str
    description: str
    duration: Optional[int]
    materials_needed: Optional[List[str]]


class TroubleshootingTip(BaseModel):
    scenario: str
    solution: str
    prevention: Optional[str]


class DeliveryTutorial(BaseModel):
    id: UUID
    project_id: UUID
    introduction: Optional[str]
    preparation_tips: Optional[List[str]]
    delivery_techniques: Optional[List[DeliveryTechnique]]
    practice_exercises: Optional[List[PracticeExercise]]
    troubleshooting: Optional[List[TroubleshootingTip]]
    generated_at: datetime
    updated_at: datetime
