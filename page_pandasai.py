import streamlit as st
import pandas as pd
from pandasai import PandasAI, SmartDataframe
from pandasai.llm.openai import OpenAI
from PIL import Image



st.set_page_config(layout="wide", initial_sidebar_state="expanded")

def app():
    
    st.image('https://images.unsplash.com/photo-1617500756598-a0ee57567ac8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&h=300&q=80')
    st.header('Experimenting with PandasAI', divider='rainbow')
    st.markdown('''
    * Using PAID OPENAI API
    * When posing a question, the entire dataframe is passed along with the question every time (be careful with large datasets)
    * [PandasAI | Github Repo](https://github.com/gventuri/pandas-ai)
    * [Medium Article](https://medium.com/@fareedkhandev/pandas-ai-the-future-of-data-analysis-8f0be9b5ab6f)
    ''')
    
    
    # Instantiate OPENAI LLM    
    llm = OpenAI(api_token=st.secrets['openai']['api_key'])
    pandas_ai = PandasAI(llm)
    
    df = pd.read_csv('assets/downloads/datasets/TickerTape_MMI_historical.csv')
    save_path = 'assets/downloads/pandasai'
    df.columns = df.columns.str.strip()
    df = df.head(200)
    st.markdown('#### Load Dataset')
    st.write(df.head())
    df = SmartDataframe(df, config={
        "llm": llm,
        "save_charts": True,
        "save_charts_path": save_path,
    })

    # Store LLM generated responses
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [{"role": "assistant", "content": "How may I help you with this dataset?"}]

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])
            
    # Function for generating LLM response
    def generate_response(question):
        return df.chat(question)

    
#    question = st.text_area('Ask question with this dataset')
    if question:= st.chat_input():
        
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.write(question)
            
        # Generate a new response if last message is not from assistant
        if st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = generate_response(question)
                    chart_terms = ['chart','image','plot','graph']
                    display_chart = max([1 for x in chart_terms if x in question.lower()] )
                    if display_chart == 1:
                        try:
                            image = Image.open('assets/downloads/pandasai/temp_chart.png')
                            st.image(image) 
                        except:
                            st.write(response)
                        
            message = {"role": "assistant", "content": response}
            st.session_state.messages.append(message)    
    
    
app()