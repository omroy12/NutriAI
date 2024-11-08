from fastapi.middleware.cors import CORSMiddleware
app = fastapi()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to specific domains if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
app = FastAPI()

# In-memory data storage
user_data = {}

# Path to save diet plans
DIET_PLAN_DIR = "diet_plans"

# Ensure the directory exists
if not os.path.exists(DIET_PLAN_DIR):
    os.makedirs(DIET_PLAN_DIR)

# Pydantic model to validate incoming data
class UserInput(BaseModel):
    age: int
    weight: float
    activity_level: str
    health_goal: str
    location: str

# Dummy function to generate a diet plan
def generate_diet_plan(user_input: dict):
    age = user_input['age']
    weight = user_input['weight']
    activity_level = user_input['activity_level']
    health_goal = user_input['health_goal']

    # Generate a simple diet plan based on user input
    plan = []
    
    if health_goal == "weight_loss":
        plan = ["Low carb meals", "Lean proteins", "Green vegetables"]
    elif health_goal == "muscle_gain":
        plan = ["High protein meals", "Complex carbs", "Strength training support"]
    else:  # Maintain health
        plan = ["Balanced diet", "Fruits and vegetables", "Moderate protein", "Whole grains"]

    return plan

# Save the diet plan to a text file
def save_diet_plan_to_file(user_id: int, diet_plan: list):
    filename = f"{DIET_PLAN_DIR}/diet_plan_user_{user_id}.txt"
    with open(filename, 'w') as f:
        f.write("Your Personalized Diet Plan:\n")
        for item in diet_plan:
            f.write(f"- {item}\n")
    return filename

# API endpoint to receive user input and return the generated diet plan
@app.post("/generate_diet_plan/")
def create_diet_plan(user_input: UserInput):
    user_id = len(user_data) + 1  # Assign a unique user ID
    user_data[user_id] = user_input.dict()

    # Generate diet plan
    diet_plan = generate_diet_plan(user_input.dict())

    if not diet_plan:
        raise HTTPException(status_code=500, detail="Failed to generate diet plan")

    # Save the diet plan to a file
    filename = save_diet_plan_to_file(user_id, diet_plan)

    # Return the generated diet plan and file name
    return {"user_id": user_id, "diet_plan": diet_plan, "file_saved": filename}

# Serve diet plan files as static files
@app.get("/diet_plan/{filename}")
def get_diet_plan_file(filename: str):
    file_path = os.path.join(DIET_PLAN_DIR, filename)
    if os.path.exists(file_path):
        return {"file": filename, "path": file_path}
    raise HTTPException(status_code=404, detail="File not found")
