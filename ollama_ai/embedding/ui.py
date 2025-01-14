#!/usr/bin/env python3
"""
    Chat Ollama Module

    Module Name: ChatOllama

    Description:
        This module is a web-based interface that uses natural language processing (NLP) techniques
        to generate human-like responses based on user input. It connects to a PostgreSQL database
        to retrieve and store knowledge graph data.

    Functions:

    *   extract_section(text): Extracts the topic relevant keywords section from a given text.
    *   remove_section(text): Removes the topic relevant keywords section from a given text.
    *   load_documents(urls): Loads documents from a list of URLs using the WebBaseLoader.
    *   embed_and_store_documents(documents): Embeds documents and stores them in PGVector.
    *   query_documents(urls, query): Queries the documents for the given question or instruction
        using the ChatOllama model.
    *   process_input(urls, q_n_a): Processes the input URLs and query to generate a response.

    Usage:
        To use this module, simply run the script and navigate to the provided URL in your browser.
        Enter URLs separated by newline characters and a question or instruction to receive a
            response.

    Requirements:
        This module requires the following dependencies: gradio, psycopg2, langchain_ollama,
        langchain_community, langchain_postgres, re, traceback, os, psycopg2.extensions

    Author:
        ©2025, Ovais Quraishi
"""

import os
import re
import traceback
from typing import List

import gradio as gr
import psycopg2
from psycopg2.extensions import make_dsn

from config import get_config
from langchain.schema import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings

from langchain_postgres import PGVector

# Configuration
CONFIG = get_config()

host = CONFIG.get('psqldb', 'host')
database = CONFIG.get('psqldb', 'database')
user = CONFIG.get('psqldb', 'user')
password = CONFIG.get('psqldb', 'password')
port = CONFIG.get('psqldb', 'port')

OLLAMA_HOST = CONFIG.get('ai', 'OLLAMA_HOST')
LLM = CONFIG.get('ai', 'LLM') or "llama3.2"

SERVICE_VERSION = CONFIG.get('service', 'version')

PGVECTOR_CONNECTION = f"postgresql+psycopg://{user}:{password}@{host}:5432/{database}"

if OLLAMA_HOST:
    os.environ['OLLAMA_HOST'] = OLLAMA_HOST
else:
    os.environ['OLLAMA_HOST'] = ""

def extract_section(text):
    """Extract Topic Relevant Keywords section"""

    pattern = r'Topic-Relevant Keywords:\n(.*?)\Z'
    match = re.search(pattern, text, re.DOTALL)
    return match.group(0).strip() if match else None

def remove_section(text):
    """Remove Topic Relevant Keywords section"""

    pattern = r'Topic-Relevant Keywords:\n(.*?)\Z'
    return re.sub(pattern, '', text, flags=re.DOTALL).strip()

def load_documents(url_list: List[str]) -> List[Document]:
    """Loads documents from a list of URLs."""

    try:
        docs = [WebBaseLoader(url).load() for url in url_list]
        return [item for sublist in docs for item in sublist]
    except Exception as e:
        print(f"Error loading documents: {e}")
        return []

def embed_and_store_documents(documents: List[Document]):
    """Embeds documents and stores them in PGVector."""

    try:
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500,
                                                                    chunk_overlap=100)
        doc_splits = text_splitter.split_documents(documents)

        embedding_model = OllamaEmbeddings(model="nomic-embed-text")
        vectorstore = PGVector.from_documents(doc_splits, embedding_model,
                                                connection=PGVECTOR_CONNECTION)

        with psycopg2.connect(make_dsn(host=host, port=port, dbname=database,
                                        user=user, password=password)) as conn:
            with conn.cursor() as cur:
                for doc in doc_splits:
                    cur.execute("SELECT id FROM rag_pgvector WHERE document = %s",
                                (doc.page_content,))
                    if not cur.fetchone():
                        vectorstore.add_documents([Document(page_content=doc.page_content)])
    except Exception as e:
        print(f"Error embedding documents: {e}\n{traceback.format_exc()}")

def query_documents(url_list: List[str], query: str) -> str:
    """Queries the documents for the given question or instruction."""

    try:
        # Load and process documents
        documents = load_documents(url_list)
        if not documents:
            return "No documents found or failed to load documents."

        embed_and_store_documents(documents)

        # Combine all document content into a single context string
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500,
                                                                    chunk_overlap=100)
        doc_splits = text_splitter.split_documents(documents)
        retriever_context = "\n".join([doc.page_content for doc in doc_splits])

        # Define prompt template
        prompt_template = """
        Based on the following context, respond to the query:
        Context: {context}
        Query: {query}
        """
        prompt = ChatPromptTemplate.from_template(prompt_template)

        # Initialize the model
        model = ChatOllama(model=LLM, temperature=0.7)

        append_query = (
            "Additionally, list 3 topic-relevant keywords as a numbered "
            "list at the end. Always label the list with exact same title "
            "'Topic-Relevant Keywords:'. This must be a list of three nothing else."
        )

        # Create the input for the pipeline
        input_data = {"context": retriever_context, "query": query + append_query}

        # Run the pipeline
        prompt_result = prompt.invoke(input_data)  # Process input through the prompt
        model_result = model.invoke(prompt_result)  # Process the prompt result through the model
        return model_result.content if hasattr(model_result, "content") else "No content available."
        #return model_result.get("content", "No content available.")
    except Exception as e:
        print(f"Error querying documents: {e}\n{traceback.format_exc()}")
        return "An error occurred while processing the query."

def process_input(urls_str: str, q_n_i: str) -> str:
    """Processes the input URLs and query to generate a response."""

    urls_list = urls_str.strip().split("\n")
    if not urls_list or not q_n_i.strip():
        return "Invalid input"

    orig_results = query_documents(urls_list, q_n_i)
    keyword_list = extract_section(orig_results)
    new_results = remove_section(orig_results)

    return new_results, keyword_list

# Define Gradio UI
with gr.Blocks(css="""
    #results-box {
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
        background-color: #737373;
        min-height: 100px;
    }
    #keywords-box {
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 5px;
        background-color: #737373;
        min-height: 100px;
    }
""", theme=gr.themes.Ocean()) as ui:
    gr.Markdown("# Chat Ollama")
    gr.Markdown("Enter URLs and a question or instruction to interact with the content.")

    with gr.Row():
        urls = gr.Textbox(label="Enter URLs (newline-separated)", lines=5)
        q_n_a = gr.Textbox(label="Question or Instruction")

    with gr.Row():
        results = gr.Markdown(elem_id="results-box", label="Results")
        keywords = gr.Markdown(elem_id="keywords-box", label="Keyword List")


    submit_button = gr.Button("Submit")
    submit_button.click(fn=process_input, inputs=[urls, q_n_a], outputs=[results, keywords])
    gr.Markdown(f"<div style='text-align: center; font-size: 1.2em;'>LLM: {LLM}<br>v{SERVICE_VERSION}</div>")
if __name__ == "__main__":
    ui.launch(server_name="0.0.0.0", pwa=True)
