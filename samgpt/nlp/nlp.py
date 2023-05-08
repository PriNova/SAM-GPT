"""This module contains the functions used to interact with the NLP model"""

from typing import List, Dict, Optional
import requests
import json
import dotenv

default_chat_config: Dict[str, any] = { # type: ignore
    "model": 'gpt-3.5-turbo',
    "max_tokens": None,
    "temperature": 0,
    "presence_penalty": 0.0,
    "top_p": 1,
    "frequency_penalty": 0,
    "stream": False
}

OPENAI_API_KEY = dotenv.get_key('.env', 'OPENAI_API_KEY')

openAI_model = ['https://api.openai.com/v1/chat/completions', OPENAI_API_KEY]
free_model = ['https://free.churchless.tech/v1/chat/completions', '']

# define the Model enum
Model = {
    'openai': openAI_model,
    'free': free_model
    }

# Get the model from the Model enu
model = Model['free']

# Get the chat completion from the model
def getChatCompletion(model, messages: List[Dict[str, str]], config: Dict[str, str], apiKey: Optional[str] = None, customHeaders: Optional[Dict[str, str]] = None):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {model[1]}'
    }

    body = {
        'messages': messages,
        **config
    }

    response = requests.post(model[0], headers=headers, data=json.dumps(body))
    response.raise_for_status()
    data = response.json()
    #To start content_without_first_linebreaks = content[2:]
    return data['choices'][0]['message']['content'].encode('utf-8').decode('utf-8')

# Start the inference
def start_inference(role, prompt):
    response = getChatCompletion(model, messages=[{'role': role, 'content': prompt}], config=default_chat_config, apiKey='')
    return response