from typing import Dict
import samgpt.nlp.nlp as nlp

# Delegation of tasks to task executors
def delegate_task(goal: str,task: Dict):
    taskDescription = task['description']
    prompt = create_task_prompt(goal, taskDescription)
    response = nlp.start_multi_prompt_inference(prompt)
    return response
    


def create_task_prompt(goal: str, taskDescription: str):
    return [{'role': 'system', 'content': f"""You are TaskMasterGPT, a task delegator that finds the best command to execute the task by choosing the best available command based on the goal and the task at hand.
Play to your strengths as an LLM and pursue simple strategies without legal complications. You answer briefly and concisely. Do not describe your actions. Only output in the format given.

Perform the following instructions carefully:

1.  From the Task delimited by triple backticks, determine which command to choose from the available commands.

```
Goal: {goal}
Task: {taskDescription}
```

Available commands (in the form of $command_name: <command description>): 

$newPlan: The CreatePlan is a command that would involve analyzing the current situation, defining objectives, identifying constraints and resources, developing action plans, and outlining tactics and communication strategies.
$webSearch: The websearch command can be used to search the web for any query or topic. It utilizes a search engine and returns relevant results based on the task.
$createCode: This command is used to write programms in HTML, CSS, JavaScript, JAVA, Python, C++, etc. for purpose of website creation, calculations, math tasks, applications and more.
$editCode: This command would allow to modify an existing codebase by opening and editing the source files. It can make the necessary changes and save the modifications to the file.
$evaluateCode: This command is used to evaluate code for pure functions or augmentable outputs.
$decomposeTask: This command is used to break down a complex task into smaller, more manageable subtasks.
$executeCode: This command can be used to execute code.
$searchTwitter: This command command is used to search for tweets on Twitter based on specific keywords, hashtags, and mentions. It can be customized to filter by location, language, date range, and more.
$tweet: This command is used to post a message (up to 280 characters) on Twitter.
$fileCRUD: This is a command-line utility that allows you to create, read, update, and delete files on your local machine. With this command, you can perform all the necessary file operations required to complete the given task like note taking, programming, memory management, todo-lists and more.
$git: Git is a distributed version control system that allows developers to manage code repositories, track changes, and collaborate with others. It provides commands for cloning, creating branches, committing changes, pushing to remote repositories, and creating pull requests.
$llm: This command can be used to perform a wide range of natural language processing tasks, including text generation, translation, sentiment analysis, and question answering, among others.
$newCommand: This command can be used to create a new command that is customized and tailored to fulfill specific tasks or goals. It allows for the creation of a unique command that can be used to perform a specific action or set of actions.

Only reply in the following format:

Command: $command_name
Thoughts: (Thoughts why the selected command is the best fit to the task)
Critics: (Constructive self-critics wether the decomposeTask command might be a better choice)
Decomposition: (Decomposing the task in the most smallest, simplest and managable numbered task list sorted by priority)
"""},
{'role': 'user', 'content': 'Choose the best command based on the task and goal. Only provide the output in the format given'}]
