import openai
import streamlit as st

# Connecting OPEN AI API
openai.api_key = st.secrets['openai']['api_key']

@st.cache_data
def get_completion(prompt, model="gpt-3.5-turbo", max_tokens=1000, temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
        temperature=temperature,  # degree of randomness of the model's output
    )
    return response.choices[0].message["content"]
