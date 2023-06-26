# A function which generates a plan based on the user's goal
from typing import List, Tuple

import nlp.nlp as nlp
from planning.plan_manager import extract_with_regex
from utils.string import format_plan_as_json


# A function which creates a highly efficient prompt includes the user's goal
def create_plan_prompt(goal) -> List:
    return [
        {
            'role': 'user',
            'content': f"""I want "{goal}" I need a plan from you. All the tasks in the plan can only be done by me with the following commands:

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

Please, give me a numbered short list of the plan sorted by priority. Do not put the commands in the plan. Do not comment or explain the plan. Here is an example how it should look like:
Plan:
1. Step One
2. Step two
3. Step three
etc.

Now it is your turn.""",
        }
    ]


def generate_plan(goal, callback) -> Tuple[str, List]:
    planPrompt = create_plan_prompt(goal)
    response: str = nlp.start_multi_prompt_inference(message=planPrompt, callback=callback)
    extractedPlan: str = extract_with_regex(response, "Plan:")
    jsonFormattedPlan: List = format_plan_as_json(extractedPlan)

    return (response, jsonFormattedPlan) if extractedPlan else ("", [])