from pydantic import BaseModel


class DeliveryTechnique(BaseModel):
    technique: str
    description: str
    when_to_use: str | None
    example: str | None


class PracticeExercise(BaseModel):
    title: str
    description: str
    duration: int | None
    materials_needed: list[str] | None


class TroubleshootingTip(BaseModel):
    scenario: str
    solution: str
    prevention: str | None
