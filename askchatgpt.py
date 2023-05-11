import streamlit as st
import openai

model_engine = "text-davinci-003"
openai.api_key =  st.secrets.openai

def askme(question):
    '''
    This function gets the question label, the project name and returns response
    This function uses the OpenAI API to generate a response to the given 
    user_query using the ChatGPT model
    '''
    response="Open AI answer"

    if question != ":q" or question != "":
     try:
      completion = openai.Completion.create(
                                  engine = model_engine,
                                  prompt = question,
                                  max_tokens = 1024,
                                  n = 1,
                                  temperature = 0.5,
                                      )
      response = completion.choices[0].text.strip()
     except openai.error.APIError as e:
      return(f'Open API returns an API Error: {e}')
      pass
     except openai.error.APIError as e:
      return(f'Open API returns an API Error: {e}')
      pass
     except openai.error.APIConnectionError as e:
      return(f'Open API returns an API Error: {e}')
      pass
     except openai.error.RateLimitError as e:
      return(f'Open API returns an API Error: {e}')
      pass
    return response
