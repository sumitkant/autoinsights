import streamlit as st
import json, requests

def app():

    st.title('ChatBot with opensource LLAMA-V2')

    API_URL = "https://api-inference.huggingface.co/models/upstage/Llama-2-70b-instruct-v2"
    hf_api_key = st.secrets['huggingface']['hf_api_key']
    headers = {"Authorization": f"Bearer {hf_api_key}"}

    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    output = query({
        "inputs": "Can you please let us know more details about your ",
    })


app()