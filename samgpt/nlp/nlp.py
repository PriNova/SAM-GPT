"""This module contains the functions used to interact with the NLP model"""

from typing import List, Dict, Optional
import requests
import json
import dotenv

defaultChatConfig: Dict[str, any] = { # type: ignore
    "model": 'gpt-3.5-turbo',
    "max_tokens": None,
    "temperature": 0,
    "presence_penalty": 0.0,
    "top_p": 1,
    "frequency_penalty": 0,
    "stream": False
}

OPENAI_API_KEY : str|None = dotenv.get_key('.env', 'OPENAI_API_KEY')

openaiModel: list = ['https://api.openai.com/v1/chat/completions', OPENAI_API_KEY]
freeModel: list = ['https://free.churchless.tech/v1/chat/completions', '']

# define the Model enum
Model: Dict = {
    'openai': openaiModel,
    'free': freeModel
    }

# Get the model from the Model enu
model: enumerate = Model['openai']

# Get the chat completion from the model
def get_chat_completion(model, messages: List[Dict[str, str]], config: Dict[str, str], apiKey: Optional[str] = None, customHeaders: Optional[Dict[str, str]] = None) -> str:
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {model[1]}'
    }

    body = {
        'messages': messages,
        **config
    }

    response = requests.post(model[0], headers=headers, data=json.dumps(body))
    repeat = 5
    while response.status_code != 200 and repeat > 0:
        response = requests.post(model[0], headers=headers, data=json.dumps(body))
        repeat -= 1
        
    #response.raise_for_status()
    data = response.json()
    #To start content_without_first_linebreaks = content[2:]
    return data['choices'][0]['message']['content'].encode('utf-8').decode('utf-8')

# Start the inference
def start__simple_inference(role, prompt) -> str:
    response = get_chat_completion(model, messages=[{'role': role, 'content': prompt}], config=defaultChatConfig, apiKey='')
    return response

def start_multi_prompt_inference(message) -> str:
    response = get_chat_completion(model, messages= message, config=defaultChatConfig, apiKey='')
    return response