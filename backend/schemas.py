from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field


class Project(BaseModel):
    id: Optional[str] = Field(default=None, description="Document ID")
    title: str
    description: str
    tech: List[str] = []
    repo_url: Optional[HttpUrl] = None
    live_url: Optional[HttpUrl] = None
    image_url: Optional[HttpUrl] = None


class Testimonial(BaseModel):
    id: Optional[str] = Field(default=None, description="Document ID")
    name: str
    role: str
    quote: str
    avatar_url: Optional[HttpUrl] = None


class Message(BaseModel):
    id: Optional[str] = Field(default=None, description="Document ID")
    name: str
    email: str
    subject: Optional[str] = None
    message: str
