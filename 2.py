from sklearn.ensemble import RandomForestClassifier
import numpy as np

# Sample data: columns represent [age, weight, activity_level (0-2), health_goal (0-2)]
X = np.array([[25, 65, 0, 1], [30, 80, 2, 0], [22, 50, 1, 2]])
y = np.array([0, 2, 1])  # Diet Plan categories

# Create a Random Forest Classifier
clf = RandomForestClassifier()
clf.fit(X, y)

# Function to predict diet plan
def predict_diet_plan(user_input):
    # Preprocess the user input
    age, weight, activity_level, health_goal = user_input["age"], user_input["weight"], user_input["activity_level"], user_input["health_goal"]
    activity_level_map = {"low": 0, "medium": 1, "high": 2}
    health_goal_map = {"weight_loss": 0, "muscle_gain": 1, "maintain_health": 2}
    
    input_data = np.array([[age, weight, activity_level_map[activity_level], health_goal_map[health_goal]]])
    diet_plan = clf.predict(input_data)
    
    return f"Diet Plan {diet_plan[0]}"
