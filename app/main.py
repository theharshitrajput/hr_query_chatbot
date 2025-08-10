from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from contextlib import asynccontextmanager
from typing import List, Dict

from .data_loader import load_employees
from .rag_system import RAGSystem

# Global variable to hold the RAG system instance
rag_pipeline = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    A lifespan event to initialize the RAG system on application startup.
    This ensures the models and data are loaded only once.
    """
    print("🚀 Server starting up...")
    global rag_pipeline
    employees_data = load_employees('employees.json')
    rag_pipeline = RAGSystem(employees_data)
    yield
    print("Server shutting down...")

# Create the FastAPI app with the lifespan manager
app = FastAPI(lifespan=lifespan)

# Pydantic models for request and response validation
class ChatQuery(BaseModel):
    query: str

class Employee(BaseModel):
    id: int
    name: str
    skills: List[str]
    experience_years: int
    projects: List[str]
    availability: str

@app.get("/")
def read_root():
    return {"message": "HR Chatbot API is running. Go to /docs for API documentation."}

@app.post("/chat")
async def chat_with_bot(request: ChatQuery):
    """Handles natural language queries to find employees using the RAG system."""
    if not rag_pipeline:
        raise HTTPException(status_code=503, detail="RAG system is not initialized.")
    
    try:
        # 1. Retrieve relevant employees
        retrieved_employees = rag_pipeline.retrieve(request.query)
        
        # 2. Generate a natural language response
        response = rag_pipeline.generate(request.query, retrieved_employees)
        
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/employees/search", response_model=List[Employee])
async def search_employees(skill: str = None, min_exp: int = None):
    """
    Simple keyword-based search for employees.
    Example: /employees/search?skill=Python&min_exp=3
    """
    if not rag_pipeline:
        raise HTTPException(status_code=503, detail="Employee data not loaded.")

    results = rag_pipeline.employees
    if skill:
        results = [emp for emp in results if skill.lower() in [s.lower() for s in emp['skills']]]
    if min_exp is not None:
        results = [emp for emp in results if emp['experience_years'] >= min_exp]
        
    return results