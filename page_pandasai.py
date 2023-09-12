import streamlit as st
import pandas as pd
from pandasai import PandasAI, SmartDataframe
from pandasai.llm.openai import OpenAI


def app():
    
    st.image('https://images.unsplash.com/photo-1617500756598-a0ee57567ac8?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D&auto=format&fit=crop&w=2070&h=600&q=80')
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
    df.columns = df.columns.str.strip()
    df = df.head(200)
    st.markdown('#### Load Dataset')
    st.write(df.head())
    df = SmartDataframe(df, config={"llm": llm})

    
    question = st.text_area('Ask question with this dataset')
    if question:
        st.markdown(f'##### {question}')
        response = df.chat(question)
        st.write(response)
    
    
    
#app()