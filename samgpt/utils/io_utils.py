import os

# Function to check if a folder exists. If it does not, it will be created.
def create_folder(folder) -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)

# Function to save the plan to a file in a specified order. If file already exists, it will be overwritten.
def save_plan(goal, plan, folder, filename) -> None:
    stripped_goal = goal.strip().replace(" ", "_")[:10]
    with open(os.path.join(stripped_goal, folder, filename), "w") as f:
        f.write(plan)