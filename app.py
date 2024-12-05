import json
from pathlib import Path
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI(
    title="Addition API",
    description="A simple API that adds two numbers together",
    version="1.0.0"
)

class Numbers(BaseModel):
    a: float
    b: float

class ContactForm(BaseModel):
    name: str
    email: str
    company: str
    message: str

@app.post("/add/", response_model=float)
async def add_numbers(numbers: Numbers):
    """
    Add two numbers together
    
    Args:
        numbers: Numbers object containing two numbers to add
        
    Returns:
        The sum of the two numbers
    """
    return numbers.a + numbers.b

@app.post("/multiply/", response_model=float)
async def multiply_numbers(numbers: Numbers):
    """
    Multiply two numbers together
    
    Args:
        numbers: Numbers object containing two numbers to multiply
        
    Returns:
        The product of the two numbers
    """
    return numbers.a * numbers.b

@app.get("/")
async def root():
    """
    Root endpoint that returns a welcome message
    """
    return {"message": "Welcome to the Addition API"}

@app.post("/contact/")
async def contact(form: ContactForm):
    """
    Handle contact form submissions
    
    Args:
        form: ContactForm object containing form data
        
    Returns:
        Success message
    """
    contact_file = Path("www.beeware.pro/contact.json")
    
    # Create file if it doesn't exist
    if not contact_file.exists():
        contact_file.write_text("[]")
        
    # Read existing contacts
    contacts = json.loads(contact_file.read_text())
    
    # Append new contact
    contacts.append(form.dict())
    
    # Write back to file
    contact_file.write_text(json.dumps(contacts, indent=2))
    
    return {"message": "Contact form submitted successfully"}
