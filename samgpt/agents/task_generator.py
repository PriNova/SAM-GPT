from typing import List
import os

import samgpt.utils.io_utils as ioutils
# track the tasks and the plan based on the users goal
def plan_tracking(goal: str, plan: str) -> None:
    tasks: List[str] = split_plan_into_tasks(plan)
    path = ioutils.get_working_dir(goal)
    save_current_task(path, tasks[0], 0)

# create a function to split the plan into a list
def split_plan_into_tasks(plan) -> List[str]:
    # split the plan into a list of tasks
    # return the list of tasks
    return plan.split("\n")

# safe current task into file
def save_current_task(workingDir: str, task: str, taskID: int) -> None:
    with open(os.path.join(workingDir, '')+f"task_{taskID}.txt", "w") as f:
        f.write(task)