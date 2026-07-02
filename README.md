# AI Document Assistant

## Project Overview

AI Document Assistant is a Streamlit-based web application that helps users understand and interact with documents more efficiently. The application allows users to upload documents, generate AI-powered summaries, translate summaries, listen to summaries using text-to-speech, and ask questions from uploaded PDF files.

This project is designed to reduce the time required to read long documents and make document analysis easier, faster, and more accessible.

## Deployed Application

Live App: Add your Streamlit deployment link here

Example:

```text
https://aipdfsummarizer-kemwr2c3zclps92qx9qmvx.streamlit.app
```

## Problem Statement

Students, professionals, and researchers often need to read large documents such as reports, notes, PDFs, and articles. Reading and understanding long documents manually can be time-consuming. It can also be difficult to quickly find important points or ask specific questions from a document.

This project solves the problem by providing an AI-based document assistant that can summarize, translate, convert text to speech, and support PDF question answering in one web application.

## Objectives

- To build a user-friendly AI document processing web application
- To summarize long text documents into short, medium, or long summaries
- To support PDF, DOCX, and TXT file uploads
- To translate summaries into different languages
- To provide text-to-speech output for generated summaries
- To allow users to ask questions from uploaded PDF documents
- To store summary history using a local database

## Key Features

- Document upload support for PDF, DOCX, and TXT files
- Manual text input option
- AI-based text summarization
- Summary length selection: Short, Medium, and Long
- Summary translation
- Text-to-speech audio generation
- PDF chatbot using vector search
- Document statistics such as word count, character count, sentence count, paragraph count, reading time, and compression percentage
- Summary download option
- Summary history storage
- Streamlit dashboard with project and system information

## Technologies Used

| Technology | Purpose |
| --- | --- |
| Python | Main programming language |
| Streamlit | Web application framework |
| Transformers | AI summarization model |
| Facebook BART | Text summarization |
| Google Gemini | PDF question answering |
| LangChain | LLM and retrieval workflow |
| FAISS | Vector database for PDF search |
| Sentence Transformers | Text embeddings |
| SQLite | Local summary history database |
| gTTS | Text-to-speech conversion |
| Deep Translator | Translation support |
| PyPDF | PDF text extraction |
| python-docx | DOCX text extraction |

## System Workflow

1. The user uploads a document or enters text manually.
2. The application extracts text from the uploaded file.
3. The user selects the required summary length and translation language.
4. The AI model generates a summary from the document text.
5. The summary is translated if a non-English language is selected.
6. The application displays document statistics.
7. The generated summary can be downloaded or converted into audio.
8. If the uploaded document is a PDF, a vector database is created.
9. The user can ask questions about the PDF using the PDF chatbot.
10. The summary details are saved in the local database for history tracking.

## Project Structure

```text
.
+-- app.py              # Main Streamlit application
+-- summarizer.py       # AI summarization logic
+-- translator.py       # Translation module
+-- tts.py              # Text-to-speech module
+-- pdf_chat.py         # PDF chatbot and vector database logic
+-- file_reader.py      # File reading utilities
+-- database.py         # SQLite database operations
+-- utils.py            # Helper functions and document statistics
+-- requirements.txt    # Required Python packages
+-- .env.example        # Environment variable example
+-- uploads/            # Uploaded documents
+-- outputs/            # Generated output files
+-- database/           # Database storage
+-- vectorstore/        # FAISS vector database
```

## Installation and Setup

1. Clone or download the project.

2. Create a virtual environment:

```bash
python -m venv venv
```

3. Activate the virtual environment:

```bash
venv\Scripts\activate
```

4. Install the required dependencies:

```bash
pip install -r requirements.txt
```

5. Create a `.env` file:

```bash
copy .env.example .env
```

6. Add your Google API key inside the `.env` file:

```env
GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY_HERE
```

7. Run the application:

```bash
streamlit run app.py
```

## How to Use

1. Open the deployed Streamlit application.
2. Upload a PDF, DOCX, or TXT file, or paste text manually.
3. Select the summary length from the sidebar.
4. Select a translation language if required.
5. Click the **Generate AI Summary** button.
6. View the original text, summary, translated summary, and document statistics.
7. Download the summary or listen to it as audio.
8. If a PDF is uploaded, ask questions using the PDF chatbot section.

## Applications

- Academic document summarization
- Research paper understanding
- Report analysis
- Notes summarization
- Multilingual document support
- Accessibility through audio summaries
- Quick PDF question answering

## Future Scope

- Add support for more file formats
- Improve chatbot memory for longer conversations
- Add user authentication
- Store user-specific document history
- Add cloud database support
- Improve UI design and mobile responsiveness
- Add OCR support for scanned PDFs and images

## Conclusion

AI Document Assistant provides an effective solution for reading, summarizing, translating, and interacting with documents. By combining AI summarization, translation, text-to-speech, and PDF question answering, the project offers a useful platform for students, professionals, and researchers who work with large documents.

## Author

Name: Sarthak Raut

Project: AI Document Assistant

Year: 2026
