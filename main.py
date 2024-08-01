import streamlit as st
# import page_aigeneratedcarousel
# import page_manualcarousel
import page_instagrampost
import page_summarizetext
import page_imagecaption
# import page_imagegeneration
# import page_pandasai
# import page_arxiv_summary
import page_speech_to_text
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader


# Page Layout
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

with open('.streamlit/config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)
    print(config)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

st.title(':rocket: Fragments.ai :rocket:')
st.write('Made with :blue_heart: & :brain: by [Sumit Kant](https://www.sumitkant.com/)')


name, authentication_status, username = authenticator.login('Login', 'main')

if authentication_status:
    authenticator.logout('Logout', 'main')
    st.write(f'Welcome *{name.split(" ")[0]}*')
    # Headings
    st.markdown('---')
    st.subheader(':warning: :warning: :warning: Using Paid API KEY!!! :warning: :warning: :warning:')
    st.subheader('Tools')

    # PAGES
    PAGES = {
        # "AI Generated Carousel": page_aigeneratedcarousel,
        # "Manual Carousel": page_manualcarousel,
        "AI Instagram Post": page_instagrampost,
        "Text Summarization": page_summarizetext,
        "Image Captioning": page_imagecaption,
        # "Image Generation": page_imagegeneration,
        # "PandasAI": page_pandasai,
        "Text to Speech": page_speech_to_text,
        # "ArXiv Paper Summary": page_arxiv_summary
    }
    selection = st.selectbox("", list(PAGES.keys()))
    st.markdown('---')

    page = PAGES[selection]
    page.app()

elif authentication_status == False:
    st.error('Username/password is incorrect')

elif authentication_status == None:
    st.warning('Please enter your username and password')

