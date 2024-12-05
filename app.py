from fastapi import FastAPI, Form
from pydantic import BaseModel, EmailStr
import json
from pathlib import Path

app = FastAPI(
    title="Addition API",
    description="A simple API that adds two numbers together",
    version="1.0.0"
)

class Numbers(BaseModel):
    a: float
    b: float

class Address(BaseModel):
    key_id: str
    street: str
    city: str
    state: str
    zip_code: str

class ContactForm(BaseModel):
    name: str
    email: EmailStr
    company: str
    message: str

@app.post("/agents/contact")
async def submit_contact(contact: ContactForm):
    """
    Handle contact form submission
    
    Args:
        contact: ContactForm object containing form details
        
    Returns:
        Confirmation message
    """
    # Create contacts directory if it doesn't exist
    Path("contacts").mkdir(exist_ok=True)
    
    # Generate unique filename using timestamp
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_path = f"contacts/contact_{timestamp}.json"
    
    # Write contact details to file
    with open(file_path, 'w') as f:
        json.dump(contact.dict(), f, indent=4)
    
    return {"message": "Thank you for your message. We will get back to you soon."}

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

@app.post("/address/update/")
async def update_address(address: Address):
    """
    Update an address for a given key ID
    
    Args:
        address: Address object containing key_id and address details
        
    Returns:
        Confirmation message
    """
    # Create addresses directory if it doesn't exist
    Path("addresses").mkdir(exist_ok=True)
    
    # Write address to file named by key_id
    file_path = f"addresses/{address.key_id}.json"
    with open(file_path, 'w') as f:
        json.dump(address.dict(), f, indent=4)
    
    return {"message": f"Address updated for key {address.key_id}"}
