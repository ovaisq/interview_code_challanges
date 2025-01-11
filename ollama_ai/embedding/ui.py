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


# Database connection details

CONFIG = get_config()

host = CONFIG.get('psqldb','host')
database = CONFIG.get('psqldb','database')
user = CONFIG.get('psqldb','user')
password = CONFIG.get('psqldb','password')
port = CONFIG.get('psqldb','port')

PGVECTOR_CONNECTION = f"postgresql+psycopg://{user}:{password}@{host}:5432/{database}"
PGVECTOR_CONNECTION2 = {
                        "host": host,
                        "port": "5432",
                        "dbname": database,
                        "user": user,
                        "password": password
                       }
dsn = make_dsn(**PGVECTOR_CONNECTION2)

os.environ['OLLAMA_HOST'] = "" #without setting this, the app will error out

def process_input(urls, query):
    model_local = ChatOllama(model="llama3.2", temperature=0.7)

    # Convert string of URLs to list
    urls_list = urls.split("\n")
    docs = [WebBaseLoader(url).load() for url in urls_list]
    docs_list = [item for sublist in docs for item in sublist]

    text_splitter = CharacterTextSplitter.from_tiktoken_encoder(chunk_size=7500, chunk_overlap=100)
    doc_splits = text_splitter.split_documents(docs_list)

    # Initialize PGVector
    try:
        # Initialize the embeddings model
        embedding_model = embeddings(model="nomic-embed-text")

        # Initialize PGVector
        vectorstore = PGVector.from_documents(doc_splits, embedding_model, connection=PGVECTOR_CONNECTION)

        # Create a new connection and use this for adding documents.
        #  We create a new connection each time so that we don't
        #  accidentally add documents using the wrong database state
        #  (e.g., if you have multiple threads).
        conn = psycopg2.connect(dsn)

        with conn:
            cur = conn.cursor()
            for doc in doc_splits:
                document = doc.page_content if hasattr(doc, 'page_content') else str(doc)
                # Check whether this document is already present
                sql_query = "SELECT id FROM rag_pgvector WHERE document = %s"
                cur.execute(sql_query, (document,))

                # If no row was returned, then the document is not yet in the table.
                if not cur.fetchone():
                    # Convert the doc to a Document object
                    new_document = Document(page_content=document)

                    # Add the document to the vector store
                    vectorstore.add_documents([new_document])

    except Exception as e:
        # Get the full traceback for debugging
        import traceback
        traceback_details = traceback.format_exc()
        print(f"Traceback Details:\n{traceback_details}")

    retriever = vectorstore.as_retriever()

    # Template for handling both questions and instructions
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
    return after_rag_chain.invoke(query)

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
    gr.Markdown("Enter URLs and a query (question or instruction) to interact with the documents.")

    with gr.Row():
        urls = gr.Textbox(label="Enter URLs separated by new lines", lines=5)
        query = gr.Textbox(label="Query (Question or Instruction)")

    results = gr.Markdown(elem_id="results-box")

    submit_button = gr.Button("Submit")
    submit_button.click(fn=process_input, inputs=[urls, query], outputs=[results])

# bind to any ip, and make it mobile friendly
ui.launch(server_name="0.0.0.0", pwa=True)
