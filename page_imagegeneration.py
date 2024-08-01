import streamlit as st
import requests
import json
import io
from PIL import Image

def app():

    def get_completion(inputs, parameters=None):
        # Hugging face API key
        hf_api_key = st.secrets['huggingface']['hf_api_key']
        headers = {
            "Authorization": f"Bearer {hf_api_key}",
            "Content-Type": "application/json"
        }
        ENDPOINT_URL = 'https://api-inference.huggingface.co/models/runwayml/stable-diffusion-v1-5'
        payload = {"inputs": inputs}
        if parameters:
            payload.update({"parameters": parameters})
        response = requests.request('POST', ENDPOINT_URL, headers=headers, data=json.dumps(payload))
        return response.content

    @st.cache_data()
    def generate_image(prompt, negative_prompt, steps, guidance, width, height):
        params = {
            "negative_prompt": negative_prompt,
            "num_inference_steps": steps,
            "guidance_scale": guidance,
            "width": width,
            "height": height
        }
        output = get_completion(prompt, params)
        return Image.open(io.BytesIO(output))

    st.title('Image generation with Stable Diffusion🧨 & Huggingface🤗')
    st.markdown("""
    * Uses a text-to-image model to generate image from input text
    * Using open source **runwayml/stable-diffusion-v1-5** using the **🧨diffusers** library
    * Model trained on set of text to image pairs
    """)
    prompt = st.text_input('Description of your image')
    c1, c2 = st.columns(2)
    negative_prompt = c1.text_input("Negative Prompt: What you don't want with the image")
    steps = c1.slider('Inference Steps: Steps to denoise the image', 1, 100, 25)
    guidance = c1.slider('Guidance Scale: Controls how much the text prompt influences the result', 1, 10, 7)
    width = c1.slider('Image Width', 64, 512, 512, 64)
    height = c1.slider('Image Height', 64, 512, 512, 64)
    if c1.button('Generate Image'):
        if prompt:
            c2.image(generate_image(prompt, negative_prompt, steps, guidance, width, height))
        else:
            c1.warning('Enter prompt')

app()