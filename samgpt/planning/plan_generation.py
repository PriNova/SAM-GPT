import re
import json
import samgpt.utils.io_utils as ioutils

# extract the plan from text
def extract_plan_with_regex(text) -> str:
    # Match numbered lists
    match = re.search(r'Plan:\n+((?:\d+.+\n?)+)', text)  # corrected regex pattern
    if match:
        plan = re.sub(r'\n?\d+\..', '\n', match.group(1)).strip()
        return plan.strip()

    # Match bulletted lists
    match = re.search(r'Plan:\n+((?:•\s*.+\n?)+)', text)
    if match:
        plan = re.sub(r'(•\s*)', '', match.group(1)).strip()
        return plan.strip()

    # Match lined lists
    match = re.search(r'Plan:\n+((?:-\s*.+\n?)+)', text)
    if match:
        plan = re.sub(r'(-\s*)', '', match.group(1)).strip()
        return plan.strip()
    
    match = re.search(r'Plan:\n+([\s\S]*?)', text)
    if match:
        plan = match.group(1).strip()
        return plan.strip()

    # No matching pattern found
    return 'No plan created'

# Format extracted plan as a JSON Object.
def formatAsJson(extractedPlan: str) -> str:
    # Split the output into tasks using newline character
    tasks = extractedPlan.strip().split("\n")

    # Create a list of dictionaries for each task
    plan = [
        {
            "id": i + 1,
            "description": task,
            "status": "Pending",
            "subtasks": []
        }
        for i, task in enumerate(tasks)
    ]
    plan_json = json.dumps(plan, indent=4)
    return plan_json