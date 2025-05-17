import streamlit as st
import json
import requests
import torch
#import openai
from transformers import AutoModelForQuestionAnswering, AutoTokenizer, pipeline, GPT2TokenizerFast, GPT2LMHeadModel
from langchain.utilities import WikipediaAPIWrapper
#import wikipedia

# this is a working version of openai interface removed after they started charging
# https://huggingface.co/deepset/xlm-roberta-large-squad2
# https://app.metatext.ai/exploreº
# https://huggingface.co/spaces/flax-community/Gpt2-bengali/commit/2d7816407af411dce0bbf868a07eb5bd6861f041

# sentence transformer
# https://huggingface.co/sentence-transformers/multi-qa-distilbert-cos-v1

#wikipedia = WikipediaAPIWrapper()
# Load the question answering model and tokenizer
#model_name = "deepset/roberta-base-squad2"
#model_name = "Xenova/gpt-3.5-turbo"
#model = GPT2LMHeadModel.from_pretrained(model_name)
#tokenizer = GPT2TokenizerFast.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained("deepset/roberta-base-squad2")
model = AutoModelForQuestionAnswering.from_pretrained("deepset/roberta-base-squad2")

nlp = pipeline('question-answering', model=model, tokenizer=tokenizer)

model_engine = "gpt-3.5-turbo"
#openai.api_key =  st.secrets.openai
API_TOKEN = st.secrets.huggingface

max_len=100
temp=80
top_k=10
top_p=0.95
do_sample=False

headers = {"Authorization": f"Bearer {API_TOKEN}"}
#API_URL = "https://api-inference.huggingface.co/models/deepset/roberta-base-squad2"
#model_name = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-large"
#url = "https://api-inference.huggingface.co/models/meta-llama/Meta-Llama-3-8B-Instruct"
#model_url = "https://huggingface.co/api/models/Xenova/gpt-3.5-turbo-16k"
#url = "https://router.huggingface.co/hf-inference/models/openai-community/gpt2"

#url = "https://api-inference.huggingface.co/models/gpt2"
#headers = {
#    "Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_KEY')}"
#}
#data = {
#    "inputs": "Once upon a time in a land far away,"
#}

#response = requests.post(url, headers=headers, json=data)
#print(response.json()[0]['generated_text'])

#def querynone(payload):
#    data = json.dumps(payload)
#    response = requests.request("POST", url, headers=headers, data=data)
#    response = requests.request("POST", MODELS[model_name]["url"], headers=headers, data=data)
#    st.write(response)
#   return json.loads(response.content.decode("utf-8"))

def query(question, context):
    # Tokenize the question and context
    inputs = tokenizer.encode_plus(question, context, add_special_tokens=True, return_tensors="pt")

    # Get the model's outputs
    outputs = model(**inputs)
    start_logits = outputs.start_logits
    end_logits = outputs.end_logits

    # Find the start and end indices of the answer
    start_index = torch.argmax(start_logits)
    end_index = torch.argmax(end_logits)

    # Convert token indices to answer text
    answer = tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs["input_ids"][0][start_index:end_index + 1]))

    return answer

def process(text: str,
            model_name: str,
            max_len: int,
            temp: float,
            top_k: int,
            top_p: float):

    payload = {
        "inputs": {
            "question": text,
            "context": "Project Management Planning",
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
    st.write(text)
    return query(text, "Project Planning")

def askme(question_input):
    # Extract keywords from the question input
    contextlist = "Project Plan"
    keywords = contextlist.split()

    # Fetch context information using the Wikipedia toolkit based on keywords
    #wikipedia = WikipediaAPIWrapper()
    #context_input = wikipedia.run(' '.join(keywords))

    # Prepare the question and context for question answering
    QA_input = {
        'question': question_input,
        'context': context_input
    }

    # Get the answer using the question answering pipeline
    res = nlp(QA_input)

    # Display the answer
    # st.write("Question:", question_input)
    # st.write("Answer:", res['answer'])
    # st.write("Score:", res['score'])
    return(res['answer'])
    

def askmehf(text):
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
#  this is not working
  return(result)

#def askme(question):
#    '''
#    This function gets the question label, the project name and returns response
#    This function uses the OpenAI API to generate a response to the given 
#    user_query using the ChatGPT model
#    disabled after free 3 month trial ended
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
