import streamlit as st
import base64
import requests
import json

def app():
    hf_api_key = st.secrets['huggingface']['hf_api_key']

    @st.cache_data
    def get_completion(inputs, parameters=None,
                       ENDPOINT_URL='https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-base'):
        headers = {
          "Authorization": f"Bearer {hf_api_key}",
          "Content-Type": "application/json"
        }
        data = {"inputs": inputs}
        if parameters is not None:
            data.update({"parameters": parameters})
        response = requests.request("POST",
                                    ENDPOINT_URL,
                                    headers=headers,
                                    data=json.dumps(data))
        return json.loads(response.content.decode("utf-8"))

    @st.cache_data
    def caption(image):
        result = get_completion(image)
        return result[0]['generated_text']


    st.title('Image Caption')
    uploads = st.file_uploader('Upload your image for captioning', type=['png', 'jpg'], accept_multiple_files=True)

    if uploads:
        for img in uploads:
            c1, c2 = st.columns((1,2))
            c1.image(img)
            i = str(base64.b64encode(img.getvalue()).decode('utf-8'))
            c2.header(caption(i))