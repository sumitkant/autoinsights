import json
import streamlit as st
from glob import glob
from libs.openai_requests import get_completion
from libs.json_to_image import generate_info_cards, generate_title_cards


# Page Layout
# st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Headings
# st.title(':rocket: Fragments.ai :rocket:')
# st.write('Made with :blue_heart: & :brain: by [Sumit Kant](https://www.sumitkant.com/)')
# st.subheader(':warning: :warning: :warning: Using Paid API KEY!!! :warning: :warning: :warning:')
# st.markdown('---')
def app():
    st.header('Manual Carousel')
    c1, c2, c3, c4 = st.columns(4)

    NUMCARDS = c1.slider('Number of Cards:', 1, 10, 5)
    TOPIC = c2.text_input('Topic')
    ATTHERATE = c3.text_input('@')
    logos = glob('assets/logos/*.png')
    LOGO = c4.selectbox('Logo:', logos)


    cols = st.columns(NUMCARDS+1)
    TITLE = cols[0].text_input(f'Title')
    SUBTITLE = cols[0].text_area(f'Subtitle', height=200)
    bg_color = cols[0].color_picker(f'Background Color', value='#000000')
    pals1 = ['#eb3b5a', '#fa8231', '#f7b731', '#20bf6b', '#0fb9b1', '#eb3b5a', '#fa8231', '#f7b731', '#20bf6b', '#0fb9b1']

    edited_response = []
    palette = []
    for card, col in zip(range(NUMCARDS+1), cols):
        if card == 0:
            pass
        else:
            h = col.text_input(f'Heading{card}')
            i = col.text_area(f'Insight{card}', height=200)
            color = col.color_picker(f'Background Color{card}', value=pals1[card-1])
            edited_response.append({'heading': h, 'insight': i, 'topic': TOPIC})
            palette.append(color)

    print(palette)

    generate_info_cards(edited_response, palette)
    generate_title_cards([TITLE], SUBTITLE, TOPIC, ATTHERATE, LOGO, factor=3, mgn=3, bg_color=bg_color, headingwrap=20)


    headingURL = glob('images/heading_*.png')[0]
    imageUrls = glob('images/card_*.png')[:NUMCARDS]
    # cols = st.columns(len(imageUrls)+1)
    cols[0].image(headingURL)
    for i, url in enumerate(imageUrls):
        cols[i+1].image(url)

    st.write(edited_response)