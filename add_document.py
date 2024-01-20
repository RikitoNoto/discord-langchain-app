import logging
import sys

from dotenv import load_dotenv
from langchain.document_loaders import UnstructuredPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from vectorstore import initialize_vectorstore

load_dotenv()

logging.basicConfig(
  format="%(asctime)s [%(levelname)s] %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

if __name__ == "__main__":
  file_path = sys.argv[1]
  loader = UnstructuredPDFLoader(file_path)
  raw_docs = loader.load()
  logger.info("Loaded %d documents", len(raw_docs))

  text_splitter = CharacterTextSplitter(chunk_size=300, chunk_overlap=30)
  docs = text_splitter.split_documents(raw_docs)
  logger.info("Split %d documents", len(docs))

  vectorstore = initialize_vectorstore()
  vectorstore.add_documents(docs)
