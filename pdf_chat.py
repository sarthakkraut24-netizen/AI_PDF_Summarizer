# ==========================================================
# PDF_CHAT.PY
# AI Document Assistant
# LangChain 1.x + Gemini + HuggingFace
# Compatible with Python 3.13+
# ==========================================================

import os
import shutil

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

# ==========================================================
# LOAD ENVIRONMENT
# ==========================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found in .env"
    )

# ==========================================================
# GEMINI MODEL
# ==========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3
)

# ==========================================================
# HUGGINGFACE EMBEDDINGS
# ==========================================================

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ==========================================================
# VECTOR DATABASE
# ==========================================================

DB_PATH = "vector_store"

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200,
    separators=[
        "\n\n",
        "\n",
        ". ",
        " "
    ]
)

# ==========================================================
# CREATE DOCUMENTS
# ==========================================================

def create_documents(
    text,
    filename="document"
):

    return [

        Document(

            page_content=text,

            metadata={

                "source": filename

            }

        )

    ]
# ==========================================================
# INDEX DOCUMENT
# ==========================================================

def index_document(
    text,
    filename="document"
):

    if not text.strip():

        return False

    documents = create_documents(
        text,
        filename
    )

    chunks = splitter.split_documents(
        documents
    )

    vectorstore = FAISS.from_documents(
        chunks,
        embeddings
    )

    if os.path.exists(DB_PATH):

        shutil.rmtree(DB_PATH)

    vectorstore.save_local(
        DB_PATH
    )

    return True


# ==========================================================
# LOAD VECTOR DATABASE
# ==========================================================

def load_database():

    if not os.path.exists(DB_PATH):

        return None

    return FAISS.load_local(

        DB_PATH,

        embeddings,

        allow_dangerous_deserialization=True

    )


# ==========================================================
# DOCUMENT INDEXED?
# ==========================================================

def is_document_indexed():

    return os.path.exists(DB_PATH)


# ==========================================================
# DATABASE INFORMATION
# ==========================================================

def database_info():

    db = load_database()

    if db is None:

        return {

            "chunks": 0

        }

    return {

        "chunks": db.index.ntotal

    }


# ==========================================================
# RESET VECTOR DATABASE
# ==========================================================

def reset_chat():

    try:

        if os.path.exists(DB_PATH):

            shutil.rmtree(DB_PATH)

        return True

    except Exception:

        return False
# ==========================================================
# CHAT WITH PDF
# ==========================================================

def chat_with_pdf(question):

    db = load_database()

    if db is None:

        return "No document has been indexed."

    try:

        # ------------------------------------------
        # Retrieve most relevant chunks
        # ------------------------------------------

        docs = db.similarity_search(

            question,

            k=4

        )

        if len(docs) == 0:

            return "No relevant information found."

        # ------------------------------------------
        # Build Context
        # ------------------------------------------

        context = "\n\n".join(

            doc.page_content

            for doc in docs

        )

        # ------------------------------------------
        # Prompt
        # ------------------------------------------

        prompt = f"""
You are an intelligent AI Document Assistant.

Answer ONLY using the information provided in the document.

If the answer is not available in the document,
reply exactly:

"I could not find this information in the uploaded document."

-------------------------
DOCUMENT
-------------------------

{context}

-------------------------
QUESTION
-------------------------

{question}

-------------------------
ANSWER
-------------------------
"""

        # ------------------------------------------
        # Gemini Response
        # ------------------------------------------

        response = llm.invoke(

            prompt

        )

        if hasattr(

            response,

            "content"

        ):

            return response.content.strip()

        return str(response)

    except Exception as e:

        return f"Error: {e}"


# ==========================================================
# SEARCH DOCUMENT
# ==========================================================

def search_document(

    keyword,

    top_k=5

):

    db = load_database()

    if db is None:

        return []

    try:

        docs = db.similarity_search(

            keyword,

            k=top_k

        )

        return [

            doc.page_content

            for doc in docs

        ]

    except Exception:

        return []


# ==========================================================
# GET ALL CHUNKS
# ==========================================================

def get_all_chunks():

    db = load_database()

    if db is None:

        return []

    try:

        docs = db.similarity_search(

            "",

            k=db.index.ntotal

        )

        return [

            doc.page_content

            for doc in docs

        ]

    except Exception:

        return []
# ==========================================================
# DOCUMENT COUNT
# ==========================================================

def document_count():

    db = load_database()

    if db is None:

        return 0

    try:

        return db.index.ntotal

    except Exception:

        return 0


# ==========================================================
# DELETE VECTOR DATABASE
# ==========================================================

def delete_database():

    try:

        if os.path.exists(DB_PATH):

            shutil.rmtree(DB_PATH)

        return True

    except Exception:

        return False


# ==========================================================
# VECTOR DATABASE EXISTS
# ==========================================================

def database_exists():

    return os.path.exists(DB_PATH)


# ==========================================================
# GET DATABASE SIZE (MB)
# ==========================================================

def database_size():

    if not os.path.exists(DB_PATH):

        return 0

    total = 0

    for root, dirs, files in os.walk(DB_PATH):

        for file in files:

            path = os.path.join(root, file)

            total += os.path.getsize(path)

    return round(total / (1024 * 1024), 2)


# ==========================================================
# DATABASE INFORMATION
# ==========================================================

def database_status():

    return {

        "exists": database_exists(),

        "chunks": document_count(),

        "size_mb": database_size()

    }


# ==========================================================
# TEST
# ==========================================================

if __name__ == "__main__":

    sample = """
Artificial Intelligence is transforming education,
healthcare, finance and agriculture.

Machine Learning allows computers to learn
from data without explicit programming.

Deep Learning is a subset of Machine Learning.
"""

    print("Creating Vector Database...")

    index_document(

        sample,

        "sample.txt"

    )

    print()

    print(

        "Database:",

        database_status()

    )

    print()

    while True:

        question = input(

            "Ask Question (type exit): "

        )

        if question.lower() == "exit":

            break

        answer = chat_with_pdf(

            question

        )

        print()

        print(answer)

        print()        