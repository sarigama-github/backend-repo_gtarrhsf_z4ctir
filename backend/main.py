from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from database import create_document, get_documents
from schemas import Project, Testimonial, Message

app = FastAPI(title="Portfolio API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class CreateProject(BaseModel):
    title: str
    description: str
    tech: List[str] = []
    repo_url: Optional[str] = None
    live_url: Optional[str] = None
    image_url: Optional[str] = None


class CreateTestimonial(BaseModel):
    name: str
    role: str
    quote: str
    avatar_url: Optional[str] = None


class CreateMessage(BaseModel):
    name: str
    email: str
    subject: Optional[str] = None
    message: str


@app.get("/test")
async def test():
    return {"status": "ok"}


@app.get("/projects", response_model=List[Project])
async def list_projects():
    return await get_documents("project")


@app.post("/projects", response_model=Project)
async def create_project(payload: CreateProject):
    return await create_document("project", payload.dict())


@app.get("/testimonials", response_model=List[Testimonial])
async def list_testimonials():
    return await get_documents("testimonial")


@app.post("/testimonials", response_model=Testimonial)
async def create_testimonial(payload: CreateTestimonial):
    return await create_document("testimonial", payload.dict())


@app.post("/contact", response_model=Message)
async def submit_message(payload: CreateMessage):
    return await create_document("message", payload.dict())
