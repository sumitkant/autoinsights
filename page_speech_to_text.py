import streamlit as st
from libs.openai_requests import generate_audio_from_text

def app():
	st.title('Text to Speech with Whisper')
	st.write('Converting given text to Speech using OPENAI Whisper. ')
	st.caption("""
	Please note that OpenAI's usage policies require you to provide a clear disclosure to end users that the TTS voice they are hearing is AI-generated and not a human voice.
	""")

	input_text = st.text_area('Enter Text to Audiofy:')
	voices = st.selectbox('Choose Voice', ['alloy', 'echo', 'fable', 'onyx', 'nova','shimmer'])
	if input_text: 
		generate_audio_from_text(input_text, voices)
		st.audio('output.mp3')


app()