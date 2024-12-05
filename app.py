import json
from pathlib import Path
from fastapi import FastAPI, Form
from pydantic import BaseModel, EmailStr
from typing import Union

app = FastAPI(
    title="Addition API",
    description="A simple API that adds two numbers together",
    version="1.0.0"
)

class Numbers(BaseModel):
    a: float
    b: float
    
class FizzBuzzInput(BaseModel):
    number: int

class ContactForm(BaseModel):
    name: str = Form(...)
    email: str = Form(...)
    company: str = Form(...)
    message: str = Form(...)

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
async def contact(
    name: str = Form(...),
    email: str = Form(...),
    company: str = Form(...),
    message: str = Form(...)
):
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
    contacts.append({
        "name": name,
        "email": email,
        "company": company,
        "message": message
    })
    
    # Write back to file
    contact_file.write_text(json.dumps(contacts, indent=2))
    
    return {"message": "Contact form submitted successfully"}

@app.post("/fizzbuzz/", response_model=Union[str, int])
async def fizz_buzz(input: FizzBuzzInput):
    """
    Implement FizzBuzz for a given number
    
    Args:
        input: FizzBuzzInput object containing the number to check
        
    Returns:
        'Fizz' if number is divisible by 3
        'Buzz' if number is divisible by 5
        'FizzBuzz' if number is divisible by both 3 and 5
        The number itself if none of the above conditions are met
    """
    number = input.number
    
    if number % 3 == 0 and number % 5 == 0:
        return "FizzBuzz"
    elif number % 3 == 0:
        return "Fizz"
    elif number % 5 == 0:
        return "Buzz"
    return number
