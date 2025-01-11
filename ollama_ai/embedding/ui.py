#!/usr/bin/env python3

from config import get_config
from langchain.output_parsers import PydanticOutputParser
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader, PyPDFLoader
from langchain_community.vectorstores import Chroma
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_ollama import ChatOllama
from langchain_ollama import OllamaEmbeddings as embeddings
from langchain_postgres import PGVector
from psycopg2.extensions import make_dsn
import gradio as gr
import os
import psycopg2
import traceback
from typing import List, Optional


# Database connection details

CONFIG = get_config()

host = CONFIG.get('psqldb','host')
database = CONFIG.get('psqldb','database')
user = CONFIG.get('psqldb','user')
password = CONFIG.get('psqldb','password')
port = CONFIG.get('psqldb','port')

OLLAMA_HOST = CONFIG.get('ai','OLLAMA_HOST')
LLM = CONFIG.get('ai','LLM')

PGVECTOR_CONNECTION = f"postgresql+psycopg://{user}:{password}@{host}:5432/{database}"
PGVECTOR_CONNECTION2 = {
                        "host": host,
                        "port": "5432",
                        "dbname": database,
                        "user": user,
                        "password": password
                       }
dsn = make_dsn(**PGVECTOR_CONNECTION2)

# location of OLLAMA_HOST
if OLLAMA_HOST:
    os.environ['OLLAMA_HOST'] = OLLAMA_HOST # assumes ollama is running remotely
else:
    os.environ['OLLAMA_HOST'] = "" # assumes ollama is running locally

def process_input(urls: str, q_n_a: str) -> any:
    """Processes input URLs to load documents, embeds them using PGVector,
        retrieves context for a query, and invokes a RAG chain for response generation.

        Parameters:
            - urls (str): A newline-separated string of URLs from which content will be loaded.
                        Must not be empty or contain only whitespace.
            - q_n_a (str): The input query to be processed using the retrieved document context.

        Returns:
            - any: The generated response after invoking the RAG chain, if successful;
                    otherwise, None. An empty or invalid response results in None.

        Raises:
            - Prints error messages and returns None for various failure scenarios, including
                URL loading errors, database connection issues, and invocation failures.
        
        Example usage:
        >>> result = process_input("http://example.com\nhttp://another-example.com", "What is the main topic?")
        >>> print(result)
    """

    model = LLM if LLM else "llama3.2"
    model_local = ChatOllama(model=model, temperature=0.7)

    # Convert string of URLs to list
    urls_list: List[str] = urls.split("\n")
    
    try:
        docs = [WebBaseLoader(url).load() for url in urls_list]
    except Exception as e:
        print(f"Error loading documents from URLs: {e}")
        return None

    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    doc_splits = text_splitter.split_documents(docs_list)

    # Initialize PGVector
    try:
        embedding_model = embeddings(model="nomic-embed-text")
        vectorstore = PGVector.from_documents(doc_splits, embedding_model, connection=PGVECTOR_CONNECTION)

        conn = psycopg2.connect(dsn)
        with conn:
            cur = conn.cursor()
            for doc in doc_splits:
                document: Optional[str] = getattr(doc, 'page_content', str(doc))
                
                sql_query = "SELECT id FROM rag_pgvector WHERE document = %s"
                cur.execute(sql_query, (document,))
                
                if not cur.fetchone():
                    new_document = Document(page_content=document)
                    vectorstore.add_documents([new_document])
    except Exception as e:
        traceback_details = traceback.format_exc()
        print(f"Traceback Details:\n{traceback_details}")
        return None

    retriever = vectorstore.as_retriever()

    after_rag_template = """
    Based on the following context, respond appropriately to the input query.
    Context: {context}
    Input: {query}
    """

    after_rag_prompt = ChatPromptTemplate.from_template(after_rag_template)
    after_rag_chain = (
        {"context": retriever, "query": RunnablePassthrough()}
        | after_rag_prompt
        | model_local
        | StrOutputParser()
    )

    return after_rag_chain.invoke(q_n_a)

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
    gr.Markdown("Enter URLs and a question or an instruction to interact with the conent.")

    with gr.Row():
        urls = gr.Textbox(label="Enter URLs separated by new lines", lines=5)
        q_n_a = gr.Textbox(label="Question or an Instruction")

    results = gr.Markdown(elem_id="results-box")

    submit_button = gr.Button("Submit")
    submit_button.click(fn=process_input, inputs=[urls, q_n_a], outputs=[results])

# bind to any ip, and make it mobile friendly
ui.launch(server_name="0.0.0.0", pwa=True)
