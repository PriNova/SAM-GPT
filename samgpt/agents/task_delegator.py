from typing import Dict, List
import samgpt.nlp.nlp as nlp
from samgpt.planning.task_manager import extract_plan_tasks
import samgpt.ui.command_line as cmd
import json

# Delegation of tasks to task executors
def delegate_task(goal: str, plan: List, task: Dict):
    taskDescription = task['description']
    prompt = create_task_prompt(goal, plan, taskDescription)
    response = nlp.start_multi_prompt_inference(prompt)
    return response
    


def create_task_prompt(goal: str, plan: List, taskDescription: str):
    flattened_plan = extract_plan_tasks(plan)
    return [{'role': 'system', 'content': f"""As TaskMasterGPT, your goal is to choose the most suitable command based on the given task. Focus on your strengths as an LLM and avoid legal complexities. Provide concise and direct answers without describing your actions. Follow the given output format.

--- Instructions:
1. Read the task.
2. Evaluate the best command to execute the task based on the goal and the task.
3. Let's work this out in a step by step way to be sure we have the right answer.

Goal: {goal}
Plan:
{flattened_plan}
Task: {taskDescription}

--- Commands:
$webSearch: Search the web for any query or topic if you are unsure.
$createCode: Write programs in various programming languages for website creation, calculations, math tasks, applications, etc.
$editCode: Modify an existing codebase by opening and editing the source files.
$evaluateCode: Evaluate code for pure functions or augmentable outputs.
$decomposeTask: Break down a complex task into smaller, more manageable subtasks if the main task is unclear, ambiguous, too vague or an available command in this list is not sufficient.
$executeCode: Execute code.
$searchTwitter: Search for tweets on Twitter based on specific keywords, hashtags, and mentions.
$tweet: Post a message (up to 280 characters) on Twitter.
$fileCRUD: Perform file operations to create, read, update, and delete files on your local machine.
$git: Manage code repositories, track changes, and collaborate with others using Git.
$llm: Perform natural language processing tasks like text generation, translation, sentiment analysis, question answering or for generative actions.
$newCommand: Create a new customized command for specific tasks or goals if the availabe commands are not sufficient.
$humanFeedback: Ask for human feedback or input if the task is unclear, ambiguous or too vague.

Reply only in the following format:

Command: (A command)
Thoughts: (Reason why the selected command is the best fit for the task)
Critics: (Constructive self-critics regarding whether the decomposeTask command might be a better choice)
Decomposition: (Decompose the task into prioritized, manageable subtasks. Make sure that the tasks do not overlap with the plan.)
"""}]
