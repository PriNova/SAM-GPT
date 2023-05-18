from samgpt.nlp.nlp import start_multi_prompt_inference
import samgpt.ui.command_line as cmd
from samgpt.nlp.nlp import start_multi_prompt_inference

from typing import List
import dotenv
import requests
import re
from bs4 import BeautifulSoup

CHAR_LIMIT = 6000

def create_answer_prompt(query: str, contents: str)-> List:
    return [{'role': 'user', 'content':  f"""Instructions:
1. Find the information's in the Text based on the Query.
2. If the Text contains the information for the query then reply with the exact answer very briefly and concise.

Search Query: {query}

Text:
'''
{contents}
'''

The result is:

"""}]

def create_summarize_prompt(query: str, contents: str)-> List:
    return [{'role': 'user', 'content':  f"""Query: "{query}"
    Text:
    '''
    {contents}
    '''

    Please distill the informations to my query based on the resulting text and reply briefly and concisely.
    The result is:
    """}]


def execute(userGoal: str, currentTaskDescription: str, callback)-> str:
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

    contents = make_web_request2(query) if query else []
    #print(contents)
    cmd.system_message('')
    cmd.system_message("SAM-GPT is collecting the responses of the web scraping!")

    cmd.system_message('')
    # summarize every scraped content from the contents list and create the final answer
    final_answer = ""
    if contents:
        result = []
        for content in contents:
            if content:
                summarize_prompt = create_summarize_prompt(query, content)
                summarize = start_multi_prompt_inference(summarize_prompt, callback)
                cmd.system_message('')
                result += summarize
        if result:
            summary = '\n'.join(result).strip()
            prompt = create_answer_prompt(query, summary)
            cmd.ai_message("\n The final answer: \n")
            final_answer = start_multi_prompt_inference(prompt, callback)
        else:
            final_answer = "Sorry, I couldn't find any information for the query!"
    else:
        final_answer = "Sorry, I couldn't find any information for the query!"
    return final_answer
        

def make_web_request2(query: str) -> List[str]:
    urls = []
    google_api = dotenv.get_key(".env", "GOOGLE_API")
    google_cx = dotenv.get_key(".env", "GOOGLE_CX")
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": f"{google_api}",
        "cx": f"{google_cx}",
        "q": f"{query}",
        "num": "5"
    }
    response = requests.get(url, params=params)
    data = response.json()
    urls = [url["link"] for url in data]
    #print(results)
    return scrape_content(urls) if urls else []

def scrape_content(results: List)-> List[str]:
    contents: List[str] = []
    for url in results:
        #try:
            response = requests.get(url)

            # parse the content with BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # find all <p> tags
            paragraphs = soup.find_all('p')
            
            # extract the text from each <p> tag and add it to a new list
            extracted_content: str = extract_text_from_paragraphs(paragraphs, CHAR_LIMIT)
            contents.append(extracted_content)
    return contents

def extract_text_from_paragraphs(paragraphs, char_limit):
    page_content = ""
    for p in paragraphs:
        page_content += ''.join(char for char in p.text if not char.isspace() or char == ' ')
    return page_content[:char_limit] + '\n'

def make_web_request(query: str) ->List[str]:
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
    print(search_results)

    search_results_list = [item["url"] for item in search_results]
    print(search_results_list)
    return scrape_content(search_results_list)

def clean_text(text: str) -> str:
    cleaned_text = re.sub("<[^>]*>", "", text)  # Remove HTML tags
    cleaned_text = cleaned_text.replace(
        "\\n", " "
    )  # Replace newline characters with spaces
    return cleaned_text

def create_search_prompt(userGoal: str, currentTaskDescription: str) -> List:
    return [
        {
            'role': 'user',
            'content': f"""I want "{userGoal}" Now I'm stuck with "{currentTaskDescription}" This task can only be done by me with a web search. I don't know how to phrase my question to get the best results when searching.

Please provide me only the query string to input into a search engine. Use the following format:
Query: (The query string to use in a search engine)

Now it's your turn.""",
        }
    ]