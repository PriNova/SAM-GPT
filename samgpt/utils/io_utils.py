import os
from typing import Dict
import json

# Function to check if a folder exists. If it does not, it will be created.
def create_folder(folder: str) -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to save the plan to a file in a specified folder. If file already exists, it will be overwritten.
def save_plan(goal: str, plan: str, filename: str) -> None:
    path = get_working_dir(goal)
    os.makedirs(path, exist_ok=True)
    with open(f'{path}/{filename}', "w") as f:
        f.write(plan)

# safe current task into file
def save_current_task(goal: str, jsonTask: Dict) -> None:
    path = get_working_dir(goal)
    with open(os.path.join(path, "task.json"), "w") as f:
        json.dump(jsonTask, f)

def get_working_dir(goal: str) -> str:
    strippedGoal = goal.strip().replace(" ", "_")[:20].lower()
    return os.path.join(strippedGoal)