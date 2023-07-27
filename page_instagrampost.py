import streamlit as st
import pandas as pd
import json
from libs.openai_requests import get_completion
from libs.json_to_image import generate_post

def app():

    st.header('Instagram Post')
    c1, c2 = st.columns((1,2))
    tones = pd.read_csv('templates/tones.csv', header=None)[0].values
    tones = [x.strip() for x in tones]

    styles = pd.read_csv('templates/writingstyles.csv', header=None)[0].values
    styles = [x.strip() for x in styles]

    TOPIC = c1.text_input('Topic')
    FIELD = c1.text_input('Field', value='Psychology')
    TONE = c1.selectbox('Tone of Voice', tones, 7)
    WRITING_STYLE = c1.selectbox('Writing Style', styles, 11)

    prompt = f"""\
    Please ignore all previous instructions. Please respond only in English Language.
    Act as an expert researcher with 20+ years in generating hard to find insights in the subject of {FIELD}. 
    You have a large fan following on instagram page that posts content about {FIELD}. 
    Generate an instagram post about the "{TOPIC}" to be shared on instagram for people who are new to {FIELD}.
    Use distinct emojis in the description and caption. 
    Use a {TONE} tone of voice and {WRITING_STYLE} writing style. 
    Use an example or an analogy as appropriate to explain the given topic. 
    MUST explain any technical term in parenthesis whenever used in MAX 7 words.
    DO NOT REPEAT YOURSELF. Do not self-reference. 
    Do not explain what you are doing. Do not explain what you are going to do.
    Generate a response in the form of JSON format with the following keys
    "title": <appropriate title>, should be catchy, viral and short
    "subtitle": <appropriate subtitle>, SHOULD BE MAX 7 WORDS LONG. MUST be a question
    "description": <explanation>, EXPLAIN IN SIMPLE TERMS IN 5 SENTENCES ABOUT {TOPIC}. NO HASHTAGS. SHOULD CONTAIN
    APPROPRIATE EMOJIS
    "caption_text": <Appropriate caption text>. Share 10 additional points about the topic. SHOULD ONLY CONTAIN TEXT. NO HASHTAGS.
    "caption_hashtags": ["hashtag1", "hashtag2", ... "hashtag25"]. MUST BE A LIST. MUST CONTAIN AT LEAST 25 HASHTAGS.
    """

    c2.subheader('Prompt')
    c2.write(prompt)

    if TOPIC:
        print('Response from chatGPT')
        response = json.loads(get_completion(prompt))
        st.markdown('---')
        # st.write(response)

        print('Formatting Response')
        st.subheader(TOPIC)
        c1, c2, c3 = st.columns((2, 2, 2))
        title = c1.text_input('Title', response['title'])
        subtitle = c1.text_input('Subtitle', response['subtitle'])
        description = c1.text_area('Description', response['description'], height=365)
        cc1, cc2, cc3 = c2.columns(3)
        bg_color = cc1.color_picker(f'Background Color', value='#000000')
        text_color = cc2.color_picker(f'Text Color', value='#ffffff')
        heading_color = cc3.color_picker(f'Heading Color', value='#ffffff')
        hashtag = c2.text_input('Hashtag', value=FIELD)
        caption = c2.text_area('Caption', response['caption_text'], height=150)
        hashtags = c2.text_area('Hashtags', ', '.join([f'#{x.lower()}' for x in response['caption_hashtags']]), height=140)

        print('Generating Image')

        img = generate_post(title, subtitle, description, color=bg_color,
                            width=2160, aspect_ratio=(1, 1), hashtag=hashtag, textcolor=text_color,
                            heading_color=heading_color)

        c3.image(img)

