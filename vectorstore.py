import os

import pinecone
from dotenv import load_dotenv
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import Pinecone


load_dotenv()


def initialize_vectorstore():
  pinecone.init(
    api_key=os.environ["PINECONE_API_KEY"],
    environment=os.environ["PINECONE_ENV"],
  )
  index_name = os.environ["PINECONE_INDEX"]
  embeddings = OpenAIEmbeddings()
  return Pinecone.from_existing_index(index_name, embeddings)
