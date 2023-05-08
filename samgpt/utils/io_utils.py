import os

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

def get_working_dir(goal: str) -> str:
    strippedGoal = goal.strip().replace(" ", "_")[:20].lower()
    return os.path.join(strippedGoal)