#!/usr/bin/env python3

import os
from config import get_config

import gradio as gr
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_postgres import PGVector
from langchain_community.vectorstores import Chroma
from langchain_ollama import OllamaEmbeddings as embeddings #new
#from langchain_community.llms.ollama import Ollama as ChatOllama
from langchain_ollama import ChatOllama #new
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from langchain.text_splitter import CharacterTextSplitter

# Database connection details

CONFIG = get_config()

host = CONFIG.get('psqldb','host')
database = CONFIG.get('psqldb','database')
user = CONFIG.get('psqldb','user')
password = CONFIG.get('psqldb','password')
port = CONFIG.get('psqldb','port')

PGVECTOR_CONNECTION = f"postgresql+psycopg://{user}:{password}@{host}:5432/{database}"
os.environ['OLLAMA_HOST'] = "http://192.168.3.16"

def process_input(urls, question):
    model_local = ChatOllama(model="qwq",temprature=0) 
    
    # Convert string of URLs to list
    urls_list = urls.split("\n")
    docs = [WebBaseLoader(url).load() for url in urls_list]
    docs_list = [item for sublist in docs for item in sublist]
    
    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    doc_splits = text_splitter.split_documents(docs_list)

    # Initialize the embeddings model
    embedding_model = embeddings(model="nomic-embed-text")

    # Initialize PGVector
    vectorstore = PGVector.from_documents(
        documents=doc_splits,
        embedding=embedding_model,
        connection=PGVECTOR_CONNECTION,
        collection_name="rag_pgvector",
    )
    retriever = vectorstore.as_retriever()

    after_rag_template = """Answer the question based only on the following context:
    {context}
    Question: {question}
    """
    after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
    after_rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | after_rag_prompt
        | model_local
        | StrOutputParser()
    )
    return after_rag_chain.invoke(question)

# Define Gradio Blocks
with gr.Blocks(css="""
    #results-box {
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
        background-color: #737373;
        min-height: 100px;
    }
""", theme=gr.themes.Ocean()) as ui:
    gr.Markdown("# Chat Ollama")
    gr.Markdown("Enter URLs and a question to query the documents.")

    with gr.Row():
        urls = gr.Textbox(label="Enter URLs separated by new lines", lines=5)
        question = gr.Textbox(label="Question")

    #results = gr.Textbox(label="Results", elem_id="markdown-output", interactive=False)
    results = gr.Markdown(elem_id="results-box")

    submit_button = gr.Button("Submit")
    submit_button.click(fn=process_input, inputs=[urls, question], outputs=[results])

ui.launch(server_name="0.0.0.0",pwa=True)
