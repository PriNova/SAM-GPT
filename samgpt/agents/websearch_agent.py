from samgpt.nlp.nlp import start_multi_prompt_inference
import samgpt.ui.command_line as cmd
from samgpt.nlp.nlp import start_multi_prompt_inference



from typing import List, Generator
import dotenv
import requests
import re
from bs4 import BeautifulSoup

CHAR_LIMIT = 2000

def create_prompt(query: str, contents: str)-> List:
    return [{'role': 'assistant', 'content':  f"""Instructions:
1. Find the information's in the Text based on the Query.
2. If the Text contains the information for the query then reply with the exact answer very briefly and concise.

Search Query: {query}

Text:
'''
{contents}
'''

The result is:

"""}]

def execute(userGoal: str, currentTaskDescription: str, callback):
    cmd.ai_message(f"Determine web search query for task: {currentTaskDescription}\n")
    prompt = create_search_prompt(userGoal, currentTaskDescription)
    response = start_multi_prompt_inference(prompt, callback)
    cmd.system_message('')
    query = ""
    match response.split():
        case ["Query:", *_]:
            query = response[5:]
        case _:
            query = ""

    content = ""
    if query:
        content = make_web_request2(query)
    cmd.system_message('')
    cmd.system_message("SAM-GPT is collecting the response!")
    prompt = create_prompt(query, content)
    response = start_multi_prompt_inference(prompt, callback)

def make_web_request2(query: str):
    results = []
    try:
        from googlesearch import search
        for j in search(query, tld="com", num=5, stop=5, pause=2):
            results.append(j)
    except ImportError:
        print("No module named 'google' found")
    #print(results)
    if results:
        contents = scrape_content(results)
        contents_flattened = ' '.join(contents).strip()
        return contents_flattened
    return ""

def scrape_content(results: List)-> List:
    contents = []
    for url in results:
        #try:
            response = requests.get(url)

            # parse the content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # find all <p> tags
            paragraphs = soup.find_all('p')
            
            # extract the text from each <p> tag and add it to a new list
            extracted_content = extract_text_from_paragraphs(paragraphs, CHAR_LIMIT)
            print(extracted_content)
            contents += extracted_content
    return contents

def extract_text_from_paragraphs(paragraphs, char_limit):
    page_content = ""
    for p in paragraphs:
        page_content += ''.join(char for char in p.text if not char.isspace() or char == ' ')
    return page_content[:char_limit] + '\n'

def make_web_request(query: str):
    bing_api = dotenv.get_key(".env", "BING_API")
    search_url = "https://api.bing.microsoft.com/v7.0/search"
    headers:  dict = {"Ocp-Apim-Subscription-Key": bing_api}
    params = {"q": query, "count": 6, "textDecorations": True, "textFormat": "HTML"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()

    # Extract the search result items from the response
    web_pages = search_results.get("webPages", {})
    search_results = web_pages.get("value", [])

    search_results_list = [item["url"] for item in search_results]
    result = scrape_content(search_results_list)
    return  result

def clean_text(text: str) -> str:
    cleaned_text = re.sub("<[^>]*>", "", text)  # Remove HTML tags
    cleaned_text = cleaned_text.replace(
        "\\n", " "
    )  # Replace newline characters with spaces
    return cleaned_text

def create_search_prompt(userGoal: str, currentTaskDescription: str) -> List:
    prompt = [{'role': 'user', 'content': f"""I want "{userGoal}" Now I'm stuck with "{currentTaskDescription}" This task can only be done by me with a web search. I don't know how to ask. I need a query string to find the best answer.

Please provide me only the query string to input into a search engine. Use the following format:
Query: (The query string to use in a search engine in a natural language style. Format the query string as a question.)

Now it's your turn."""}]
    return prompt