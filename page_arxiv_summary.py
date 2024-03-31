import streamlit as st
import arxiv
import fitz #pymupdf
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.document_loaders import TextLoader
from langchain.indexes import VectorstoreIndexCreator

        
#@st.cache_data()
#def load_research_paper(q):
#    documents = ArxivLoader(query=q, load_max_docs=10).load()
#    st.info(len(documents))
#    return documents[0].metadata, documents[0].page_content

#def load_arxiv_paper(arxiv_id):
#    search = arxiv.Search(id_list=[arxiv_id])

def app():

    saved_pdf_path = "assets/downloads/arxiv/downloaded-paper.pdf"
    persist_directory = 'assets/downloads/langchain/chroma'

    # @st.cache_data()
    def load_and_save_paper(q):
        search = arxiv.Search(query=q)
        paper = next(search.results())
        paper.download_pdf(filename=saved_pdf_path)
        return paper

    def pdf_to_text():
        doc = fitz.open(saved_pdf_path) # open a document
        content = []
        for page in doc: # iterate the document pages
            text = page.get_text() # get plain text encoded as UTF-8
            content.append(text)
        content = '\n\n'.join(content)
        return content


        
    st.title('Summarize Research Papers')
    c1,c2 = st.columns(2)
    query = c1.text_input('ARXIV ID:', value='1910.03225')
    
    # METADATA    
    metadata = load_and_save_paper(query)
    authors = ', '.join([str(x) for x in metadata.authors])
    st.title(metadata.title)
    st.caption(f"{metadata.published.date()}: {authors}")
    st.write(metadata.summary)

    
    # CONTENT
    st.subheader('Content')
    converted_text = pdf_to_text()
    st.caption(converted_text[:1000]+"...")
    st.write(f'Content Length: {len(converted_text)}')
    
        
    # VECTOR STORE
    # loader = TextLoader(converted_text)
    # index = VectorstoreIndexCreator().from_loaders([loader])
    
        

app()