import openai
import streamlit as st
from openai import OpenAI

# Connecting OPEN AI API
# openai.api_key = st.secrets['openai']['api_key']
client = OpenAI(api_key=st.secrets['openai']['api_key']) 

@st.cache_data
def get_completion(prompt, model="gpt-3.5-turbo", max_tokens=1000, temperature=0):
    messages = [{"role": "user", "content": prompt}]
    response = client.chat.completions.create(
        model=model,
        max_tokens=max_tokens,
        messages=messages,
        temperature=temperature,  # degree of randomness of the model's output
    )
    return response.choices[0].message.content



def generate_audio_from_text(input_text, voice):
	response = client.audio.speech.create(
	    model="tts-1",
	    voice=voice,
	    input=input_text,
	)

	return response.stream_to_file("output.mp3")