from datetime import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

from api.models import type_str


class EmailAnalysisDetailsBase(BaseModel):
    attachments: List[type_str] = Field(description="A list of the email attachment names")

    cc_addresses: List[type_str] = Field(description="A list of CC recipient email addresses")

    from_address: type_str = Field(description="The email sender's address")

    message_id: type_str = Field(description="The email's message-id")

    reply_to_address: Optional[type_str] = Field(description="The reply-to email address")

    subject: Optional[type_str] = Field(description="The email's subject")

    time: datetime = Field(description="The time the email was received")

    to_address: type_str = Field(description="The recipient's email address")


class EmailAnalysisDetails(EmailAnalysisDetailsBase):
    """Represents the fields in Email Analysis details that the frontend expects for event pages."""

    body_html: Optional[type_str] = Field(description="The HTML body of the email")

    body_text: Optional[type_str] = Field(description="The plaintext body of the email")

    headers: type_str = Field(description="The headers of the email")
