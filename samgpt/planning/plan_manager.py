import re
import json

# extract the plan from text
def extract_with_regex(text, prefix: str) -> str:
    # Match numbered lists
    match = re.search(fr'{prefix}\n+((?:\d+.+\n?)+)', text)  # corrected regex pattern
    if match:
        plan = re.sub(r'\n?\d+\..', '\n', match.group(1)).strip()
        return plan.strip()

    # Match bulletted lists
    match = re.search(fr'{prefix}\n+((?:•\s*.+\n?)+)', text)
    if match:
        plan = re.sub(r'(•\s*)', '', match.group(1)).strip()
        return plan.strip()

    # Match lined lists
    match = re.search(fr'{prefix}\n+((?:-\s*.+\n?)+)', text)
    if match:
        plan = re.sub(r'(-\s*)', '', match.group(1)).strip()
        return plan.strip()
    
    match = re.search(fr'{prefix}\n+([\s\S]*?)', text)
    if match:
        plan = match.group(1).strip()
        return plan.strip()

    # No matching pattern found
    return 'Not successfully extracted!'

# Format extracted plan as a JSON Object.
def set_status_for_task(plan_json: str, task_id: int, status: str) -> str:
    plan = json.loads(plan_json)
    for task in plan:
        if task["id"] == task_id:
            task["status"] = status
    return json.dumps(plan, indent=4)