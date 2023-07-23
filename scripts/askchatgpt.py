import streamlit as st
import re
import json
import requests
#import openai

# https://huggingface.co/deepset/xlm-roberta-large-squad2
# https://app.metatext.ai/exploreº
# https://huggingface.co/spaces/flax-community/Gpt2-bengali/commit/2d7816407af411dce0bbf868a07eb5bd6861f041

model_engine = "text-davinci-003"
#openai.api_key =  st.secrets.openai
API_TOKEN = st.secrets.huggingface

max_len=100
temp=80
top_k=10
top_p=0.95
do_sample=False

headers = {"Authorization": f"Bearer {API_TOKEN}"}
#API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
model_name = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
model_name = "https://api-inference.huggingface.co/models/deepset/xlm-roberta-large-squad2"

def query(payload):
    data = json.dumps(payload)
    response = requests.request("POST", model_name, headers=headers, data=data)
#    response = requests.request("POST", MODELS[model_name]["url"], headers=headers, data=data)
    st.write(response)
    return json.loads(response.content.decode("utf-8"))
def process(text: str,
            model_name: str,
            max_len: int,
            temp: float,
            top_k: int,
            top_p: float):

    payload = {
        "inputs": {
            "question": text,
            "context": "A Project management plan.",
        },
        "parameters": {
            "max_new_tokens": max_len,
            "top_k": top_k,
            "top_p": top_p,
            "temperature": temp,
            "repetition_penalty": 2.0,
        },
        "options": {
            "use_cache": True,
        }
    }
    st.write(payload)
    return query(payload)

def askme(text):

  answer=""
  result = process(text=text,
                         model_name=model_name,
                         max_len=int(max_len),
                         temp=temp,
                         top_k=int(top_k),
                         top_p=float(top_p))
  if "error" in result:
            st.write(result)
            if type(result["error"]) is str:
                st.write(f'{result["error"]}.', end=" ")
                if "estimated_time" in result:
                    st.write(f'Please try it again in about {result["estimated_time"]:.0f} seconds')
            else:
                if type(result["error"]) is list:
                    for error in result["error"]:
                        st.write(f'{error}')
                else:
                  answer = result[0]["generated_text"]
                  st.write(result.replace("\n", "  \n"))
  return(result)
#  return(result[answer])

#def askme(question):
#    '''
#    This function gets the question label, the project name and returns response
#    This function uses the OpenAI API to generate a response to the given 
#    user_query using the ChatGPT model
#    '''
#    response="Open AI answer"
#    st.write(question)
#    st.write(response)
#    if question != ":q" or question != "":
#     try:
#      completion = openai.Completion.create(
#                                  engine = model_engine,
#                                  prompt = question,
#                                  max_tokens = 1024,
#                                  n = 1,
#                                  temperature = 0.5,
#                                      )
#      response = completion.choices[0].text.strip()
#     except openai.error.APIError as e:
#      return(f'Open API returns an API Error: {e}')
#      pass
#     except openai.error.APIError as e:
#      return(f'Open API returns an API Error: {e}')
#      pass
#     except openai.error.APIConnectionError as e:
#      return(f'Open API returns an API Error: {e}')
#      pass
#     except openai.error.RateLimitError as e:
#      return(f'Open API returns an API Error: {e}')
#      pass
#    re.sub(r'^$\n', '', response, flags=re.MULTILINE)
#    return response
