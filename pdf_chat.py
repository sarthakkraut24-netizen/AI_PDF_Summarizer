# ==========================================================
# PDF CHAT MODULE
# AI Document Assistant
# Part 1 - PDF Processing & Vector Database
# Compatible with Python 3.13+
# ==========================================================

import os
from dotenv import load_dotenv
from pypdf import PdfReader

from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings

# ==========================================================
# LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError(
        "GOOGLE_API_KEY not found. Please add it to your .env file."
    )

# ==========================================================
# VECTOR DATABASE CONFIGURATION
# ==========================================================

VECTOR_FOLDER = "vectorstore"

os.makedirs(VECTOR_FOLDER, exist_ok=True)

# ==========================================================
# READ PDF
# ==========================================================

def read_pdf(pdf_path):

    try:

        reader = PdfReader(pdf_path)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

        return text.strip()

    except Exception as e:

        raise Exception(f"Error reading PDF:\n{e}")

# ==========================================================
# SPLIT TEXT INTO CHUNKS
# ==========================================================

def split_text(text):

    splitter = RecursiveCharacterTextSplitter(

        chunk_size=1000,

        chunk_overlap=200,

        length_function=len

    )

    return splitter.split_text(text)

# ==========================================================
# LOAD EMBEDDING MODEL
# ==========================================================

def load_embeddings():

    try:

        embeddings = HuggingFaceEmbeddings(

            model_name="sentence-transformers/all-MiniLM-L6-v2"

        )

        return embeddings

    except Exception as e:

        raise Exception(f"Embedding Model Error:\n{e}")

# ==========================================================
# CREATE VECTOR DATABASE
# ==========================================================

def create_vector_database(pdf_path):

    text = read_pdf(pdf_path)

    if not text.strip():

        raise Exception("No text found inside PDF.")

    chunks = split_text(text)

    embeddings = load_embeddings()

    vector_db = FAISS.from_texts(

        texts=chunks,

        embedding=embeddings

    )

    vector_db.save_local(VECTOR_FOLDER)

    return True

# ==========================================================
# LOAD VECTOR DATABASE
# ==========================================================

def load_vector_database():

    if not os.path.exists(VECTOR_FOLDER):

        raise FileNotFoundError(
            "Vector database not found."
        )

    embeddings = load_embeddings()

    vector_db = FAISS.load_local(

        VECTOR_FOLDER,

        embeddings,

        allow_dangerous_deserialization=True

    )

    return vector_db

# ==========================================================
# CHECK VECTOR DATABASE
# ==========================================================

def vector_database_exists():

    return os.path.exists(VECTOR_FOLDER)
# ==========================================================
# GOOGLE GEMINI LLM
# ==========================================================

import google.generativeai as genai

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.documents import Document

# ==========================================================
# CONFIGURE GEMINI
# ==========================================================

genai.configure(
    api_key=GOOGLE_API_KEY
)

# ==========================================================
# LOAD GEMINI MODEL
# ==========================================================

def load_llm():

    try:

        llm = ChatGoogleGenerativeAI(

            model="gemini-2.5-flash",

            temperature=0.3,

            google_api_key=GOOGLE_API_KEY

        )

        return llm

    except Exception as e:

        raise Exception(f"Gemini Model Error:\n{e}")

# ==========================================================
# CREATE RETRIEVER
# ==========================================================

def create_retriever():

    vector_db = load_vector_database()

    retriever = vector_db.as_retriever(

        search_type="similarity",

        search_kwargs={

            "k": 4

        }

    )

    return retriever

# ==========================================================
# LOAD CHATBOT
# ==========================================================

def load_chatbot():

    retriever = create_retriever()

    llm = load_llm()

    return {
        "retriever": retriever,
        "llm": llm
    }

# ==========================================================
# ASK QUESTION
# ==========================================================

def ask_question(chatbot, question):

    if not question.strip():
        return "Please enter a valid question."

    try:

        docs = chatbot["retriever"].invoke(question)

        context = "\n\n".join(
            doc.page_content for doc in docs
        )

        prompt = f"""
Use ONLY the context below to answer the question.

Context:
{context}

Question:
{question}

Answer:
"""

        response = chatbot["llm"].invoke(prompt)

        return response.content

    except Exception as e:

        return f"Error: {e}"

# ==========================================================
# ASK QUESTION WITH SOURCES
# ==========================================================

def ask_with_sources(chatbot, question):

    docs = chatbot["retriever"].invoke(question)

    context = "\n\n".join(
        doc.page_content for doc in docs
    )

    prompt = f"""
Use ONLY the context below.

Context:
{context}

Question:
{question}

Answer:
"""

    response = chatbot["llm"].invoke(prompt)

    return response.content, docs

# ==========================================================
# SEARCH DOCUMENTS
# ==========================================================

def search_documents(question):

    db = load_vector_database()

    docs = db.similarity_search(

        question,

        k=4

    )

    return docs

# ==========================================================
# GET DOCUMENT COUNT
# ==========================================================

def total_chunks():

    db = load_vector_database()

    return db.index.ntotal
# ==========================================================
# CHAT HISTORY
# ==========================================================

chat_history = []


def get_chat_history():

    return chat_history


def clear_chat_history():

    global chat_history

    chat_history.clear()


# ==========================================================
# CHAT WITH PDF
# ==========================================================

def chat_with_pdf(question):

    chatbot = load_chatbot()

    answer = ask_question(chatbot, question)

    chat_history.append({

        "question": question,

        "answer": answer

    })

    return answer


# ==========================================================
# MULTIPLE PDF SUPPORT
# ==========================================================

def create_multiple_pdf_database(pdf_files):

    all_text = ""

    for pdf in pdf_files:

        try:

            all_text += read_pdf(pdf) + "\n"

        except Exception:

            continue

    if not all_text.strip():

        raise Exception("No readable PDF files found.")

    chunks = split_text(all_text)

    embeddings = load_embeddings()

    vector_db = FAISS.from_texts(

        texts=chunks,

        embedding=embeddings

    )

    vector_db.save_local(VECTOR_FOLDER)

    return True


# ==========================================================
# REBUILD VECTOR DATABASE
# ==========================================================

def rebuild_vector_database(pdf_path):

    delete_vector_database()

    return create_vector_database(pdf_path)


# ==========================================================
# DELETE VECTOR DATABASE
# ==========================================================

def delete_vector_database():

    if not os.path.exists(VECTOR_FOLDER):

        return False

    for file in os.listdir(VECTOR_FOLDER):

        file_path = os.path.join(

            VECTOR_FOLDER,

            file

        )

        try:

            os.remove(file_path)

        except Exception:

            pass

    return True


# ==========================================================
# VECTOR DATABASE INFORMATION
# ==========================================================

def vector_database_info():

    exists = os.path.exists(VECTOR_FOLDER)

    total_files = 0

    if exists:

        total_files = len(os.listdir(VECTOR_FOLDER))

    return {

        "exists": exists,

        "folder": VECTOR_FOLDER,

        "files": total_files

    }


# ==========================================================
# TEST VECTOR DATABASE
# ==========================================================

def test_database():

    try:

        db = load_vector_database()

        return {

            "status": True,

            "chunks": db.index.ntotal

        }

    except Exception as e:

        return {

            "status": False,

            "error": str(e)

        }
# ==========================================================
# HEALTH CHECK
# ==========================================================

def system_health():

    report = {}

    report["Google API"] = GOOGLE_API_KEY is not None

    report["Vector Database"] = vector_database_exists()

    try:

        report["Embedding Model"] = load_embeddings() is not None

    except Exception:

        report["Embedding Model"] = False

    return report


# ==========================================================
# CHATBOT STATUS
# ==========================================================

def chatbot_ready():

    try:

        load_chatbot()

        return True

    except Exception:

        return False


# ==========================================================
# PRINT SYSTEM STATUS
# ==========================================================

def print_status():

    info = system_health()

    print("\n========== SYSTEM STATUS ==========\n")

    for key, value in info.items():

        print(f"{key} : {value}")

    print("\n===================================\n")


# ==========================================================
# STANDALONE TEST
# ==========================================================

if __name__ == "__main__":

    print("\nAI Document Assistant")
    print("------------------------------")

    print_status()

    pdf_file = "sample.pdf"

    if os.path.exists(pdf_file):

        print("\nCreating Vector Database...")

        try:

            create_vector_database(pdf_file)

            print("Vector Database Created Successfully.")

        except Exception as e:

            print(e)

        if chatbot_ready():

            chatbot = load_chatbot()

            while True:

                question = input("\nAsk a question (type 'exit' to quit): ")

                if question.lower() == "exit":

                    break

                answer = ask_question(

                    chatbot,

                    question

                )

                print("\nAnswer:\n")

                print(answer)

        else:

            print("Chatbot could not be loaded.")

    else:

        print("\nsample.pdf not found.")

    print("\nProgram Finished.")