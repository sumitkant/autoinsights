import streamlit as st
import requests


def app():
    hf_api_key = st.secrets['huggingface']['hf_api_key']
    headers = {"Authorization": f"Bearer {hf_api_key}"}

    @st.cache_data(show_spinner='Generating Summary...')
    def query(payload, API_URL):
        response = requests.post(API_URL, headers=headers, json=payload)
        return response.json()

    @st.cache_data
    def get_model_details(API_URL):
        return requests.get(API_URL).json()

    c1, c2, c3 = st.columns((2,3,2))
    dummy_input = f"""\
    The tower is 324 metres (1,063 ft) tall, about the same height as an 81-storey building, 
    and the tallest structure in Paris. Its base is square, measuring 125 metres (410 ft) on each side. 
    During its construction, the Eiffel Tower surpassed the Washington Monument to become the tallest man-made 
    structure in the world, a title it held for 41 years until the Chrysler Building in New York City was 
    finished in 1930. It was the first structure to reach a height of 300 metres. Due to the addition of a broadcasting  
    aerial at the top of the tower in 1957, it is now taller than the Chrysler Building by 5.2 metres (17 ft). 
    Excluding transmitters, the Eiffel Tower is the second tallest free-standing structure 
    in France after the Millau Viaduct.
    """

    c1.subheader('Model')
    API_URL = 'https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6'
    model_details = get_model_details(API_URL)
    c1.write(API_URL)
    # c1.write(model_details)
    #c1.image(model_details['cardData']['thumbnail'])

    c2.subheader('Text to Summarize')
    input = c2.text_area('Text', height=350, value=dummy_input)
    button = c2.button('Summarize')
    c3.subheader('Summary')

    if not input:
        c2.error('Add text to summarize')
    summary = query({"inputs": f"{input}"}, API_URL)
    c3.text_area('Output', key='key_output', value=summary[0]['summary_text'], height=250)


