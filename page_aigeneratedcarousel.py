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
    TONE = c1.selectbox('Tone of Voice', tones, 7)
    WRITING_STYLE = c1.selectbox('Writing Style', styles, 11)
    FIELD = c1.text_input('Field', value='Psychology')
    TOPIC = c2.text_input('Topic')
    SLIDES = c1.slider('Number of Slides:', 1, 10, 8)
    # CHARACTERS = c1.slider('Number of Characters:', 50, 500, 200, step=50)

    delimiter = "####"
    prompt_research = f"""\
    Please respond only in English Language.
    Act as an expert researcher with 20+ years in generating hard to find insights in the subject of {FIELD}. 
    You have a large fan following on instagram page that posts content about {FIELD}. 
    Use a {TONE} tone of voice and {WRITING_STYLE} writing style.
    Given a topic delimited by the {delimiter}, generate an instagram carousel with exactly {SLIDES} slides
    Each slide MUST be a JSON object with 3 ELEMENTS
    "title": <appropriate title>, should be catchy, viral and short
    "subtitle": <appropriate subtitle>, SHOULD BE MAX 7 WORDS LONG
    "description": <explanation>, EXPLAIN IN SIMPLE TERMS IN 5 SENTENCES the title of that slide. Use distinct emojis.
    Use an example or an analogy as appropriate to explain a slide.
    the description MUST explain any technical term in parenthesis whenever used in MAX 7 words.
    DO NOT REPEAT YOURSELF. Do not self-reference. 
    Do not explain what you are doing. Do not explain what you are going to do.
    generate your response in the form of a LIST with each item being a slide.
    The last two items in the list MUST BE a caption for instagram carousel. The caption should contain 10 additional
    points about the topic WIHOUT USING ANY HASHTAGS.
    The list item should a list at least 25 hashtags separated by comma.
    PLEASE CHECK THE FORMAT FOR JSON OBJECT BEFORE GENERATING A RESPONSE. KEYS MUST BE IN DOUBLE QUOTES
    The topic is #### {TOPIC} ####
    """

    c2.subheader('Prompt')
    c2.write(prompt_research)

    # if c2.button('Generate Content'):
    st.markdown('---')
    st.subheader(TOPIC)
    if TOPIC:
        response_research = get_completion(prompt_research, model=MODEL)
        response_research = json.loads(response_research)
        # st.write(response_research)
        slides = response_research[:-2]
        captions = response_research[-2]
        hashtags = response_research[-1]
        hashtags = ' '.join(f'#{x.strip().lower()}' for x in hashtags.split(','))
        c1, c2 = st.columns(2)
        c1.text_area('Captions', value=captions)
        c2.text_area('Hashtags', value=hashtags)
        palettes = {
            'Psych Lab (Dark)': ['#545454', '#ffffff', '#31BD93'],
            'Psych Lab (Light)': ['#ffffff', '#545454', '#31BD93'],
            'Study Lab (Dark)': ['#000000', '#ffffff', '#FF914D'],
            'Study Lab (Light)': ['#ffffff', '#000000', '#FF914D'],
            'Design Lab (Light)': ['#ffffff', '#545454', '#DF207A'],
            'Bluestone (Light)': ['#ffffff', '#004AAD', '#004AAD'],
            'Bluestone (Dark)': ['#004AAD', '#ffffff', '#ffffff'],
        }
        palette = c1.selectbox('Color Palette', palettes.keys())
        cols = st.columns(len(slides))
        for i, (slide, col) in enumerate(zip(slides, cols)):
            h = col.text_input(f'Title {i+1}', value=slide['title'])
            s = col.text_input(f'Sub Title {+1}', value=slide['subtitle'])
            c = col.text_area(f'Insight {i+1}', height=400, value=slide['description'])
            bg_color = col.color_picker(f'Background Color {i+1}', value=palettes[palette][0])
            text_color = col.color_picker(f'Text Color {i+1}', value=palettes[palette][1])
            heading_color = col.color_picker(f'Heading Color {i+1}', value=palettes[palette][2])
            img = generate_card(h, c, color=bg_color, width=2160, aspect_ratio=(1, 1), num=i+1,
                                textcolor=text_color, heading_color=heading_color)
            col.image(img)


    #     # CREATE IMAGES FROM JSON
    #     cols = st.columns(len(response_research))
    #     pals1 = ['#eb3b5a', '#fa8231', '#f7b731', '#20bf6b', '#0fb9b1', '#eb3b5a', '#fa8231', '#f7b731', '#20bf6b', '#0fb9b1']
    #     pals2 = ['#ffffff']*10
    #
    #     # POINTS = 5
    #     edited_response = []
    #     palette = []
    #     for card, col in zip(range(len(response_research)), cols):
    #         h = col.text_input(f'Heading{card}', value=response_research[card]['heading'])
    #         c = col.text_area(f'Insight{card}', height=300, value=response_research[card]['content'])
    #         color = col.color_picker(f'Background Color{card}', value=pals2[card-1])
    #         edited_response.append({'heading': h, 'content': c, 'color': color})
    #
    #     # st.write(edited_response)
    #
    #     for card, col in zip(range(len(edited_response)), cols):
    #         generate_card(edited_response[card]['heading'], edited_response[card]['content'],
    #                       color=edited_response[card]['color'], width=2160, aspect_ratio=(1, 1), num=card+1, textcolor='#545454')
    #         col.image(f'images/card_{card+1}.png')
    #
    #
    # # Act as an expert in psychology and neuroscience which a large fan following on instagram. Given a topic, generate an instagram post content to be shared on instagram for people who are new to psychology. Use a friendly tone of voice and informative writing style. Use the following format for your response.
    # # Title: <>
    # # Subtitle: <>. SHOULD BE MAX 7 WORDS.
    # # Description: <>. A 300 chracter description on the topic
    # # Caption: A corresponding caption for the topic in 200 characters.
    # # hashtags: <>. A list of about 20 hashtags to be used at the end of captions. ALL HASHTAGS should be in small letters