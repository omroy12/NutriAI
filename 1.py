from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import requests

app = FastAPI()

# In-memory data storage (to be replaced with Vultr cloud)
user_data = {}
food_availability_data = {}

# Sample Model for User Input
class UserInput(BaseModel):
    age: int
    weight: float
    activity_level: str
    health_goal: str
    dietary_preferences: List[str]
    location: str

# Sample User Feedback Model
class Feedback(BaseModel):
    user_id: int
    feedback: str

# Dummy ML Model (could be more complex)
def generate_diet_plan(user_input):
    # Example of how you might generate a diet plan based on activity level
    plans = {
        "low": ["Plan A", "Plan B"],
        "medium": ["Plan C", "Plan D"],
        "high": ["Plan E", "Plan F"]
    }
    return plans[user_input['activity_level']]

# Add User Data and Get Diet Plan
@app.post("/generate_diet_plan/")
def create_diet_plan(user_input: UserInput):
    # Save user data in memory (or store in Vultr cloud)
    user_id = len(user_data) + 1
    user_data[user_id] = user_input.dict()

    # Get local food availability (dummy function, could use Vultr cloud storage here)
    food_data = get_local_food_availability(user_input.location)

    # Generate diet plan using simple ML logic (can be replaced with advanced model)
    diet_plan = generate_diet_plan(user_input.dict())
    
    return {"user_id": user_id, "diet_plan": diet_plan, "local_food": food_data}

# Example to Get Local Food Availability
def get_local_food_availability(location):
    # This function could call a real-time API or use pre-stored data
    # Dummy data for now
    return ["Apples", "Bananas", "Carrots"] if location == "region_a" else ["Mangoes", "Papayas", "Tomatoes"]

# Feedback Endpoint
@app.post("/feedback/")
def add_feedback(feedback: Feedback):
    user_id = feedback.user_id
    if user_id not in user_data:
        raise HTTPException(status_code=404, detail="User not found")
    # Log feedback and potentially update the plan (dummy implementation)
    print(f"Received feedback from User {user_id}: {feedback.feedback}")
    return {"message": "Feedback received, thank you!"}

# Start the server with Uvicorn
# Command: uvicorn main:app --reload
