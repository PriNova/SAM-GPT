from typing import Dict
import samgpt.nlp.nlp as nlp

# Delegation of tasks to task executors
def delegate_task(goal: str,task: Dict):
    taskDescription = task['description']
    prompt = create_task_prompt(goal, taskDescription)
    response = nlp.start_multi_prompt_inference(prompt)
    return response
    


def create_task_prompt(goal: str, taskDescription: str):
    return [{'role': 'system', 'content': f"""As TaskMasterGPT, your goal is to choose the most suitable command based on the given task. Focus on your strengths as an LLM and avoid legal complexities. Provide concise and direct answers without describing your actions. Follow the given output format.

Perform the following instructions carefully:

1. Determine the best command to choose from the available commands based on the goal and task description.

Goal: {goal}
Task: {taskDescription}

Available commands:

$createPlan: Analyze the current situation, define objectives, identify constraints and resources, develop action plans, and outline tactics and communication strategies.
$webSearch: Search the web for any query or topic.
$createCode: Write programs in various programming languages for website creation, calculations, math tasks, applications, etc.
$editCode: Modify an existing codebase by opening and editing the source files.
$evaluateCode: Evaluate code for pure functions or augmentable outputs.
$decomposeTask: Break down a complex task into smaller, more manageable subtasks.
$executeCode: Execute code.
$searchTwitter: Search for tweets on Twitter based on specific keywords, hashtags, and mentions.
$tweet: Post a message (up to 280 characters) on Twitter.
$fileCRUD: Perform file operations like create, read, update, and delete files on your local machine.
$git: Manage code repositories, track changes, and collaborate with others using Git.
$llm: Perform natural language processing tasks like text generation, translation, sentiment analysis, and question answering.
$newCommand: Create a new customized command for specific tasks or goals.
$humanFeedback: Ask for human feedback or input if the task is unclear or ambiguous.

Reply in the following format:

Command: $command_name
Thoughts: (Reason why the selected command is the best fit for the task)
Critics: (Constructive self-critics regarding whether the decomposeTask command might be a better choice)
Decomposition: (Decompose the task into a prioritized, manageable task list)
"""},
{'role': 'user', 'content': 'Choose the best command based on the task and goal. Only provide the output in the format given'}]
