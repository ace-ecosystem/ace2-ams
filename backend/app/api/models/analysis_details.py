from datetime import datetime
from pydantic import BaseModel, Field, IPvAnyAddress
from typing import List, Optional

from api.models import type_str


class EmailAnalysisDetailsHeaderBody(BaseModel):
    body_html: Optional[type_str] = Field(description="The HTML body of the email")

    body_text: Optional[type_str] = Field(description="The plaintext body of the email")

    headers: type_str = Field(description="The headers of the email")


class EmailAnalysisDetailsBase(BaseModel):
    attachments: List[type_str] = Field(description="A list of the email attachment names")

    cc_addresses: List[type_str] = Field(description="A list of CC recipient email addresses")

    from_address: type_str = Field(description="The email sender's address")

    message_id: type_str = Field(description="The email's message-id")

    reply_to_address: Optional[type_str] = Field(description="The reply-to email address")

    subject: Optional[type_str] = Field(description="The email's subject")

    time: datetime = Field(description="The time the email was received")

    to_address: type_str = Field(description="The recipient's email address")


class EmailAnalysisDetails(EmailAnalysisDetailsBase, EmailAnalysisDetailsHeaderBody):
    """Represents the minimum fields in Email Analysis details that the frontend expects for event pages."""

    pass


class FAQueueAnalysisDetails(BaseModel):
    """Represents the minimum fields in FA Queue Analysis details that the frontend expects for event pages."""

    hits: int = Field(description="The number of hits produced by the FA Queue search for the observable")

    link: Optional[type_str] = Field(description="A link (such as to Splunk) where the FA Queue search can be viewed")


class SandboxContactedHost(BaseModel):
    """Represents a contacted host from a sandbox report."""

    ip: IPvAnyAddress = Field(description="The IP address of the contacted host")

    port: Optional[int] = Field(description="The TCP/UDP port used when contacting the host")

    protocol: Optional[type_str] = Field(description="The protocol used when contacting the host (usually TCP or UDP)")

    location: Optional[type_str] = Field(description="Where the host is located")

    associated_domains: List[type_str] = Field(description="A list of domains associated with the contacted host")


class SandboxDnsRequest(BaseModel):
    """Represents a DNS request from a sandbox report."""

    request: type_str = Field(description="The domain that was requested")

    type: Optional[type_str] = Field(description="The type of the DNS request (usually 'A')")

    answer: Optional[type_str] = Field(description="The result of the DNS request")

    answer_type: Optional[type_str] = Field(description="The type of the DNS request answer")


class SandboxDroppedFile(BaseModel):
    """Represents a dropped file from a sandbox report."""

    filename: type_str = Field(description="The name of the dropped file")

    path: Optional[type_str] = Field(description="The path where the file was dropped")

    size: Optional[int] = Field(description="The size (in bytes) of the dropped file")

    type: Optional[type_str] = Field(description="The type of the dropped file")

    md5: Optional[type_str] = Field(description="The MD5 hash of the dropped file")

    sha1: Optional[type_str] = Field(description="The SHA1 hash of the dropped file")

    sha256: Optional[type_str] = Field(description="The SHA256 hash of the dropped file")

    sha512: Optional[type_str] = Field(description="The SHA512 hash of the dropped file")

    ssdeep: Optional[type_str] = Field(description="The SSDEEP hash of the dropped file")


class SandboxHttpRequest(BaseModel):
    """Represents an HTTP request from a sandbox report."""

    host: type_str = Field(description="The HTTP host that was contacted")

    port: Optional[int] = Field(description="The HTTP port used in the request")

    path: Optional[type_str] = Field(description="The path that was requested")

    method: Optional[type_str] = Field(description="The HTTP method used for the request")

    user_agent: Optional[type_str] = Field(description="The user-agent used for the request")


class SandboxProcess(BaseModel):
    """Represents an executed process from a sandbox report."""

    command: type_str = Field(description="The command that was executed")

    pid: int = Field(description="The process ID")

    parent_pid: int = Field(description="The parent process' ID")

    children: List["SandboxProcess"] = Field(description="A list of child processes", default_factory=list)


class SandboxAnalysisDetails(BaseModel):
    """Represents the minimum fields in the Sandbox Analysis details that the frontend expects for event pages."""

    contacted_hosts: List[SandboxContactedHost] = Field(
        description="A list of contacted hosts during the sandbox execution", default_factory=list
    )

    created_services: List[type_str] = Field(
        description="A list of services that were created during the sandbox execution", default_factory=list
    )

    dns_requests: List[SandboxDnsRequest] = Field(
        description="A list of DNS requests made during the sandbox execution", default_factory=list
    )

    dropped_files: List[SandboxDroppedFile] = Field(
        description="A list of dropped files from the sandbox execution", default_factory=list
    )

    filename: type_str = Field(description="The name of the sandboxed file")

    http_requests: List[SandboxHttpRequest] = Field(
        description="A list of HTTP requests made during the sandbox execution", default_factory=list
    )

    malware_family: str = Field(description="The malware family as identified from the sandbox", default="")

    md5: type_str = Field(description="The MD5 hash of the sandboxed file", default="")

    memory_strings: List[type_str] = Field(description="A list of strings found in memory", default_factory=list)

    memory_urls: List[type_str] = Field(description="A list of URLs found in memory", default_factory=list)

    mutexes: List[type_str] = Field(
        description="A list of mutexes created during the sandbox execution", default_factory=list
    )

    processes: List[SandboxProcess] = Field(
        description="A list of the executed processes during the sandbox execution", default_factory=list
    )

    registry_keys: List[type_str] = Field(
        description="A list of registry keys accessed or modified during the sandbox execution", default_factory=list
    )

    resolved_apis: List[type_str] = Field(
        description="A list of APIs used during the sandbox execution", default_factory=list
    )

    sandbox_url: type_str = Field(description="A URL where the sandbox report can be viewed")

    sha1: str = Field(description="The SHA1 hash of the sandboxed file", default="")

    sha256: str = Field(description="The SHA256 hash of the sandboxed file", default="")

    sha512: str = Field(description="The SHA512 hash of the sandboxed file", default="")

    ssdeep: str = Field(description="The SSDEEP hash of the sandboxed file", default="")

    started_services: List[type_str] = Field(
        description="A list of services that were started during the sandbox execution", default_factory=list
    )

    strings_urls: List[type_str] = Field(
        description="A list of URLs found in the strings of the sandboxed file", default_factory=list
    )

    suricata_alerts: List[type_str] = Field(
        description="A list of Suricata alerts identified during the sandbox execution", default_factory=list
    )


class UserAnalysisDetails(BaseModel):
    """Represents the minimum fields in User Analysis details that the frontend expects for event pages."""

    company: Optional[type_str] = Field(description="The company to which the user belongs")

    department: Optional[type_str] = Field(description="The department to which the user belongs")

    division: Optional[type_str] = Field(description="The division to which the user belongs")

    email: type_str = Field(description="The user's email address")

    manager_email: Optional[type_str] = Field(description="The email address of the user's manager")

    title: Optional[type_str] = Field(description="The user's job title")

    user_id: type_str = Field(description="The user's user ID")


# This is needed for the circular relationship between SandboxProcess
SandboxProcess.update_forward_refs()
