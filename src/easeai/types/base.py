from enum import Enum


class ProjectPhase(str, Enum):
    PREPARATION = "preparation"
    GENERATION = "generation"
    REVIEW = "review"
    COMPLETE = "complete"


class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"


class ProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"
