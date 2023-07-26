import streamlit as st
import page_aigeneratedcarousel
import page_manualcarousel
import page_instagrampost

# Page Layout
st.set_page_config(layout="wide", initial_sidebar_state="expanded")

# Headings
st.title(':rocket: Fragments.ai :rocket:')
st.write('Made with :blue_heart: & :brain: by [Sumit Kant](https://www.sumitkant.com/)')
st.subheader(':warning: :warning: :warning: Using Paid API KEY!!! :warning: :warning: :warning:')
st.subheader('Tools')

# PAGES
PAGES = {
    "AI Generated Carousel": page_aigeneratedcarousel,
    "Manual Carousel": page_manualcarousel,
    "AI Instagram Post": page_instagrampost
}
selection = st.selectbox("", list(PAGES.keys()))
st.markdown('---')

page = PAGES[selection]
page.app()
