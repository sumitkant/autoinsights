import streamlit as st
from langchain.document_loaders.generic import GenericLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

def app():
    st.title('Summarize Youtube Videos')
    url = st.text_input('YouTube URL:')
    if url:
        st.video(url)
        save_dir = "assets/downloads/YouTube"
        loader = GenericLoader(YoutubeAudioLoader([url], save_dir), OpenAIWhisperParser())
        docs = loader.load()
    else:
        st.info('Input URL')

app()