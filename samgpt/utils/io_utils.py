import os
from typing import Dict
import json

# Function to check if a folder exists. If it does not, it will be created.
def create_folder(folder) -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to save the plan to a file in a specified folder. If file already exists, it will be overwritten.
def save_plan(goal, plan, filename) -> None:
    path = get_working_dir(goal)
    if not os.path.exists(path):
        create_folder(path)
    with open(os.path.join(path, '')+filename, "w") as f:
        f.write(plan)

# safe current task into file
def save_current_task(goal: str, jsonTask: Dict) -> None:
    path = get_working_dir(goal)
    taskID = jsonTask['id']
    task = json.dumps(jsonTask)
    with open(os.path.join(path, '')+f"task_{taskID}.json", "w") as f:
        f.write(task)

def get_working_dir(goal: str) -> str:
    strippedGoal = goal.strip().replace(" ", "_")[:20].lower()
    return os.path.join(strippedGoal)