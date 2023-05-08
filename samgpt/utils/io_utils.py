import os

# Function to check if a folder exists. If it does not, it will be created.
def create_folder(folder) -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to save the plan to a file in a specified order. If file already exists, it will be overwritten.
def save_plan(goal, plan, filename) -> None:
    strippedGoal = goal.strip().replace(" ", "_")[:20].lower()
    path = os.path.join(strippedGoal)
    if not os.path.exists(path):
        create_folder(path)
    with open(os.path.join(path, '')+filename, "w") as f:
        f.write(plan)