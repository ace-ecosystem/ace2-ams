from datetime import datetime
from pydantic import BaseModel, Field, UUID4
from uuid import uuid4

from api_models import type_str
from api_models.user import UserRead


class SubmissionCommentBase(BaseModel):
    """Represents a comment that can be added to a submission."""

    submission_uuid: UUID4 = Field(description="The UUID of the submission associated with this comment")

    value: type_str = Field(description="The value of the comment")


class SubmissionCommentCreate(SubmissionCommentBase):
    username: type_str = Field(description="The username of the user creating the comment")

    uuid: UUID4 = Field(default_factory=uuid4, description="The UUID of the comment")


class SubmissionCommentRead(SubmissionCommentBase):
    insert_time: datetime = Field(description="The time the comment was made")

    user: UserRead = Field(description="The user that created the comment")

    uuid: UUID4 = Field(description="The UUID of the comment")

    class Config:
        orm_mode = True


class SubmissionCommentUpdate(BaseModel):
    username: type_str = Field(description="The username of the user updating the comment")

    # The only thing that makes sense to be able to update is the actual value of the comment.
    # Otherwise, you would delete the comment and create a new comment on a submission.
    value: type_str = Field(description="The value of the comment")
