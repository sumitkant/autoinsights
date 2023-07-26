import json
import streamlit as st
import pandas as pd
from glob import glob
from libs.openai_requests import get_completion
from libs.json_to_image import generate_info_cards, generate_title_cards, generate_card


def app():
    st.header('AI Generated Carousel')
    templates = ['Instagram Post', 'Instagram Carousel']
    tones = pd.read_csv('templates/tones.csv', header=None)[0].values
    tones = [x.strip() for x in tones]
    styles = pd.read_csv('templates/writingstyles.csv', header=None)[0].values
    styles = [x.strip() for x in styles]

    c1, c2 = st.columns((1, 2))
    MODEL = c1.selectbox('Model', ['gpt-3.5-turbo', 'gpt-4'], 0)
    CATEGORY = c1.selectbox('Category', templates, 1)
    TONE = c1.selectbox('Tone of Voice', tones, 7)
    WRITING_STYLE = c1.selectbox('Writing Style', styles, 11)
    TOPIC = c2.text_input('Topic')
    SLIDES = c1.slider('Number of Slides:', 1, 10, 8)
    CHARACTERS = c1.slider('Number of Characters:', 50, 500, 200, step=50)

    delimiter = "####"
    prompt_research = f"""\
    Please ignore all previous instructions. Please respond only in English Language.
    You are an instagrammer with large fan following. You have a {TONE} tone of voice. 
    You have a {WRITING_STYLE} writing style. Create an {CATEGORY} on "{TOPIC}".
    There should be exactly {SLIDES} slides. Generate the slides as a list of JSON objects.
    Each JSON object should contain two keys - "heading" and "content".
    The heading should be the exact heading without any slide numbers. 
    The content should be the insight or the description of the heading in about {CHARACTERS} characters.
    Try to use multiple unique emojis in the content. Within each slide try to give an example or
    explain through a simple analogy.
    The last item in the list should be an instagram post description with keys exactly same keys - "heading","content".
    The "content" for description should be instagram caption in just a few sentences for {CATEGORY} topic with emoji's 
    and instagram hashtags (in SMALL LETTERS) at the end. The description should have a hook and entice the readers
    Do not repeat yourself. Do not self-reference. Do not explain what you are doing. 
    Do not explain what you are going to do. Start directly by writing down the slide details.
    Do not mention slide numbers in the heading.
    Check for syntax in the JSON object before presenting the output.
    """

    c2.subheader('Prompt')
    c2.write(prompt_research)

    # if c2.button('Generate Content'):
    st.markdown('---')
    st.subheader(TOPIC)
    if TOPIC:
        response_research = json.loads(get_completion(prompt_research, model=MODEL))
        # st.write(response_research)

        # CREATE IMAGES FROM JSON
        cols = st.columns(len(response_research))
        pals1 = ['#eb3b5a', '#fa8231', '#f7b731', '#20bf6b', '#0fb9b1', '#eb3b5a', '#fa8231', '#f7b731', '#20bf6b', '#0fb9b1']
        pals2 = ['#ffffff']*10

        # POINTS = 5
        edited_response = []
        palette = []
        for card, col in zip(range(len(response_research)), cols):
            h = col.text_input(f'Heading{card}', value=response_research[card]['heading'])
            c = col.text_area(f'Insight{card}', height=300, value=response_research[card]['content'])
            color = col.color_picker(f'Background Color{card}', value=pals2[card-1])
            edited_response.append({'heading': h, 'content': c, 'color': color})

        # st.write(edited_response)

        for card, col in zip(range(len(edited_response)), cols):
            generate_card(edited_response[card]['heading'], edited_response[card]['content'],
                          color=edited_response[card]['color'], width=2160, aspect_ratio=(1, 1), num=card+1, textcolor='#545454')
            col.image(f'images/card_{card+1}.png')


    # Act as an expert in psychology and neuroscience which a large fan following on instagram. Given a topic, generate an instagram post content to be shared on instagram for people who are new to psychology. Use a friendly tone of voice and informative writing style. Use the following format for your response.
    # Title: <>
    # Subtitle: <>. SHOULD BE MAX 7 WORDS.
    # Description: <>. A 300 chracter description on the topic
    # Caption: A corresponding caption for the topic in 200 characters.
    # hashtags: <>. A list of about 20 hashtags to be used at the end of captions. ALL HASHTAGS should be in small letters