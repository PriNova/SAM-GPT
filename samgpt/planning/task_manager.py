from typing import List, Dict
from typing import Tuple

# track the tasks and the plan based on the users goal
def get_task(plan: List, index: int) -> Dict:
    #jsonPlan: Dict = json.loads(plan)
    if index < len(plan):
        return plan[index]
    return {}

# create a function to split the plan into a list
def split_plan_into_tasks(plan) -> List[str]:
    # split the plan into a list of tasks
    # return the list of tasks
    return plan.split("\n")


# Filter out all tasks by status
def filter_plan_for_tasks(jsonPlan, filter: str) -> List:
    return [task for task in jsonPlan if task["status"] == filter]

# Update the plan by replacing the task with the updated task
def update_task_by_id(plan: List, task_id: str, updated_info: Dict):
    # Convert the task and optional sub-task indices to integers
    task_index = int(task_id.split(".")[0]) - 1

    # Check if the task ID has a sub-task index
    if "." in task_id:
        subtask_index = int(task_id.split(".")[1]) - 1
    else:
        subtask_index = None

    if subtask_index is not None:
        # Update a sub-task
        for key, value in updated_info.items():
            plan[task_index]["tasks"][subtask_index][key] = value
    else:
        # Update a task
        for key, value in updated_info.items():
            plan[task_index][key] = value

    # Return the updated plan
    return plan


# Approves a task by setting the status to "In Progress" and updating the plan
def approve_task(cPlan: List, currentTask: Dict) -> Tuple[List, Dict, str]:
    currentTask['status'] = "In Progress"
    cPlan = find_and_update_task(cPlan, currentTask['id'], {'status': currentTask['status']})
    return cPlan, currentTask, "Task approved."

# Modifies a task by updating the description and updating the plan
def modify_task(cPlan, currentTask, newDescription: str):
    currentTask['description'] = newDescription
    cPlan = find_and_update_task(cPlan, currentTask['id'], {'description': currentTask['description']})
    return cPlan, currentTask, "Task modified"

# Skipping a task by setting the status to "Skipped", updating the plan and fetch the next task
def skip_task(cPlan, currentTask):
    currentTask['status'] = "Skipped"
    cPlan = find_and_update_task(cPlan, currentTask['id'], {'status': currentTask['status']})
    newTask = find_next_pending_task(cPlan, currentTask['id'])
    return cPlan, newTask, "Task skipped."

def find_and_update_task(tasks: List, task_id: str, updated_info: Dict):
    for task in tasks:
        if task["id"] == task_id:
            # Update task
            for key, value in updated_info.items():
                task[key] = value
        else:
            # Go through each sub-task
            for subtask in task["tasks"]:
                find_and_update_task(subtask, task_id, updated_info)
    return tasks

def find_and_add_subtask(tasks: List, parent_task_id: str, new_subtask: List):
    for task in tasks:
        if task["id"] == parent_task_id:
            # Add new sub-task
            task["tasks"].append(new_subtask)
        else:
            # Go through each sub-task
            for subtask in task["tasks"]:
                find_and_add_subtask(subtask, parent_task_id, new_subtask)

def find_next_pending_task(tasks: List, index: str) -> Dict:
    # Parse the start index into a list of integers
    if index == '0': return {}
    start_index: List = [int(x) - 1 for x in index.split(".")] if index else [0]

    # Get the next task index
    next_index: int = start_index[-1] + 1 if start_index else 0

    # Get the parent tasks
    parent_tasks: List = tasks
    for i in start_index[:-1]:
        parent_tasks = parent_tasks[i]["tasks"]

    # Check the remaining tasks at the current level
    for i in range(next_index, len(parent_tasks)):
        if parent_tasks[i]["status"] == "Pending":
            return parent_tasks[i]
        elif parent_tasks[i]["tasks"]:
            next_pending = find_next_pending_task(parent_tasks[i]["tasks"], "0")
            if next_pending:
                return next_pending

    # No more tasks at the current level, go up one level
    if start_index:
        new_index = ".".join(map(str, start_index[:-1])) if start_index[:-1] else "0"
        return find_next_pending_task(tasks, new_index)
    # All tasks are completed
    return {}

def update_parent_task_status(task):
    if all(subtask["status"] == "completed" for subtask in task["tasks"]):
        task["status"] = "completed"
    for subtask in task["tasks"]:
        update_parent_task_status(subtask)
