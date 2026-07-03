import html
import os
from pathlib import Path

import streamlit as st

from database import create_database, load_history, save_history
from export import export_file
from file_reader import read_file
from ocr import extract_text_from_scanned_pdf
from pdf_chat import (
    chat_with_pdf,
    database_info,
    index_document,
    is_document_indexed,
    reset_chat,
)
from summarizer import AISummarizer
from table_reader import extract_tables
from translator import get_languages, translate_text
from tts import text_to_speech
from utils import character_count, reading_time, word_count


SUPPORTED_TYPES = [
    "pdf",
    "docx",
    "txt",
    "pptx",
    "xlsx",
    "xls",
    "png",
    "jpg",
    "jpeg",
]


st.set_page_config(
    page_title="AI Document Assistant",
    page_icon=":material/description:",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_styles():
    st.markdown(
        """
        <style>
            :root {
                --ink: #172033;
                --muted: #64748b;
                --line: #dbe3ef;
                --panel: #ffffff;
                --soft: #f6f8fb;
                --teal: #0f766e;
                --teal-dark: #115e59;
                --amber: #b45309;
                --blue: #1d4ed8;
                --rose: #be123c;
            }

            .stApp {
                background:
                    radial-gradient(circle at 18% 0%, rgba(15, 118, 110, 0.12), transparent 28rem),
                    radial-gradient(circle at 92% 12%, rgba(180, 83, 9, 0.10), transparent 22rem),
                    linear-gradient(180deg, #f8fafc 0%, #eef3f8 100%);
                color: var(--ink);
            }

            [data-testid="stSidebar"] {
                background: #0f172a;
            }

            [data-testid="stSidebar"] * {
                color: #e5eefb;
            }

            [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p,
            [data-testid="stSidebar"] label {
                color: #cbd5e1;
            }

            [data-testid="stSidebar"] .stSelectbox div[data-baseweb="select"] > div,
            [data-testid="stSidebar"] .stFileUploader section {
                border-color: rgba(226, 232, 240, 0.24);
                background: rgba(15, 23, 42, 0.48);
            }

            .block-container {
                max-width: 1320px;
                padding-top: 1.4rem;
                padding-bottom: 3rem;
            }

            h1, h2, h3 {
                letter-spacing: 0;
            }

            div[data-testid="stMetric"] {
                background: rgba(255, 255, 255, 0.86);
                border: 1px solid var(--line);
                border-radius: 8px;
                padding: 1rem 1.05rem;
                box-shadow: 0 16px 40px rgba(15, 23, 42, 0.06);
            }

            div[data-testid="stMetricLabel"] p {
                color: var(--muted);
                font-size: 0.82rem;
            }

            .hero {
                border: 1px solid rgba(219, 227, 239, 0.92);
                border-radius: 8px;
                padding: 1.45rem;
                background:
                    linear-gradient(135deg, rgba(255,255,255,0.96), rgba(255,255,255,0.82)),
                    linear-gradient(135deg, rgba(15,118,110,0.18), rgba(29,78,216,0.14));
                box-shadow: 0 24px 70px rgba(15, 23, 42, 0.08);
                margin-bottom: 1rem;
            }

            .eyebrow {
                color: var(--teal-dark);
                font-weight: 800;
                font-size: 0.78rem;
                text-transform: uppercase;
                margin-bottom: 0.35rem;
            }

            .hero-title {
                color: var(--ink);
                font-size: clamp(2rem, 4vw, 3.8rem);
                line-height: 1.02;
                font-weight: 850;
                margin: 0;
            }

            .hero-copy {
                color: #475569;
                font-size: 1.02rem;
                max-width: 760px;
                margin-top: 0.75rem;
            }

            .status-strip {
                display: flex;
                flex-wrap: wrap;
                gap: 0.55rem;
                margin-top: 1rem;
            }

            .status-pill {
                border: 1px solid var(--line);
                border-radius: 999px;
                background: #fff;
                color: #334155;
                font-size: 0.82rem;
                font-weight: 700;
                padding: 0.42rem 0.72rem;
            }

            .section-kicker {
                color: var(--muted);
                font-size: 0.85rem;
                font-weight: 700;
                text-transform: uppercase;
                margin: 0 0 0.25rem 0;
            }

            .empty-state {
                border: 1px dashed #b6c3d4;
                border-radius: 8px;
                background: rgba(255,255,255,0.72);
                color: #475569;
                padding: 1.25rem;
            }

            .summary-box {
                border-left: 4px solid var(--teal);
                background: #ffffff;
                border-radius: 8px;
                padding: 1rem 1.1rem;
                border-top: 1px solid var(--line);
                border-right: 1px solid var(--line);
                border-bottom: 1px solid var(--line);
                white-space: pre-wrap;
                line-height: 1.65;
            }

            .input-panel {
                border: 1px solid var(--line);
                border-radius: 8px;
                background: rgba(255, 255, 255, 0.86);
                padding: 1rem 1.1rem 1.15rem;
                box-shadow: 0 18px 44px rgba(15, 23, 42, 0.06);
                margin-bottom: 1rem;
            }

            .chat-row {
                border: 1px solid var(--line);
                border-radius: 8px;
                background: #ffffff;
                padding: 1rem;
                margin-bottom: 0.75rem;
            }

            .chat-question {
                color: var(--blue);
                font-weight: 800;
                margin-bottom: 0.35rem;
            }

            .chat-answer {
                color: #334155;
                line-height: 1.6;
                white-space: pre-wrap;
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 0.35rem;
            }

            .stTabs [data-baseweb="tab"] {
                border-radius: 8px 8px 0 0;
                padding: 0.7rem 1rem;
                background: rgba(255, 255, 255, 0.68);
                border: 1px solid var(--line);
                border-bottom: 0;
            }

            .stButton > button,
            .stDownloadButton > button {
                border-radius: 8px;
                border: 1px solid rgba(15, 118, 110, 0.28);
                font-weight: 800;
            }

            .stButton > button[kind="primary"] {
                background: linear-gradient(135deg, var(--teal), var(--blue));
                border: 0;
            }

            textarea {
                border-radius: 8px !important;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


@st.cache_resource
def load_model():
    return AISummarizer()


def ensure_session_state():
    defaults = {
        "summary": "",
        "translated_text": "",
        "uploaded_text": "",
        "uploaded_filename": "",
        "uploaded_extension": "",
        "pasted_text_input": "",
        "chat_history": [],
        "language": "English",
        "tables": [],
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def human_file_size(size_bytes):
    if not size_bytes:
        return "0 KB"

    size_kb = size_bytes / 1024
    if size_kb < 1024:
        return f"{size_kb:.1f} KB"

    return f"{size_kb / 1024:.2f} MB"


def render_hero():
    status = "Indexed" if is_document_indexed() else "Not indexed"
    active_file = html.escape(st.session_state.uploaded_filename or "No document loaded")
    summary_state = "Summary ready" if st.session_state.summary else "Awaiting summary"

    st.markdown(
        f"""
        <section class="hero">
            <div class="eyebrow">Document intelligence workspace</div>
            <h1 class="hero-title">AI Document Assistant</h1>
            <p class="hero-copy">
                Upload a document, generate a focused summary, translate it, listen to it,
                export it, and ask questions from the same polished workspace.
            </p>
            <div class="status-strip">
                <span class="status-pill">{active_file}</span>
                <span class="status-pill">{summary_state}</span>
                <span class="status-pill">Vector search: {status}</span>
            </div>
        </section>
        """,
        unsafe_allow_html=True,
    )


def render_metrics(text, summary):
    indexed_chunks = database_info()["chunks"] if is_document_indexed() else 0
    compression = "0%"
    if text and summary and word_count(text):
        compression = f"{round((1 - (word_count(summary) / word_count(text))) * 100)}%"

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Document words", f"{word_count(text):,}")
    col2.metric("Reading time", f"{reading_time(text)} min")
    col3.metric("Summary words", f"{word_count(summary):,}")
    col4.metric("Indexed chunks", f"{indexed_chunks:,}", compression)


def load_uploaded_document(uploaded_file):
    extension = Path(uploaded_file.name).suffix.lower()
    text = read_file(uploaded_file)

    if not text.strip() and extension == ".pdf":
        uploaded_file.seek(0)
        text = extract_text_from_scanned_pdf(uploaded_file)

    tables = []
    if extension == ".pdf":
        uploaded_file.seek(0)
        tables = extract_tables(uploaded_file)

    st.session_state.uploaded_text = text
    st.session_state.uploaded_filename = uploaded_file.name
    st.session_state.uploaded_extension = extension
    st.session_state.tables = tables
    st.session_state.summary = ""
    st.session_state.translated_text = ""


def load_pasted_text(text):
    st.session_state.uploaded_text = text.strip()
    st.session_state.uploaded_filename = "Pasted paragraph"
    st.session_state.uploaded_extension = ".txt"
    st.session_state.tables = []
    st.session_state.summary = ""
    st.session_state.translated_text = ""
    st.session_state.chat_history.clear()


def render_sidebar():
    with st.sidebar:
        st.markdown("### Controls")
        summary_type = st.segmented_control(
            "Summary length",
            ["Short", "Medium", "Long"],
            default="Medium",
        )

        language = st.selectbox("Translate to", get_languages(), index=0)
        st.session_state.language = language

        st.divider()
        st.markdown("### Search index")
        if is_document_indexed():
            info = database_info()
            st.success(f"Ready with {info['chunks']} chunks")
        else:
            st.info("No indexed document yet")

        if st.button("Reset document index", use_container_width=True):
            reset_chat()
            st.session_state.chat_history.clear()
            st.toast("Document index reset")
            st.rerun()

        if st.button("Clear chat", use_container_width=True):
            st.session_state.chat_history.clear()
            st.toast("Chat cleared")

    return summary_type, language


def render_document_input():
    with st.container(border=True):
        st.markdown('<p class="section-kicker">Start here</p>', unsafe_allow_html=True)
        file_col, text_col = st.columns([1, 1], gap="large")

        with file_col:
            uploaded_file = st.file_uploader(
                "Upload a document",
                type=SUPPORTED_TYPES,
                help="PDF, DOCX, TXT, PPTX, XLSX, XLS, PNG, JPG, or JPEG.",
                key="main_file_upload",
            )

            if uploaded_file is not None:
                st.caption(f"{uploaded_file.name} - {human_file_size(uploaded_file.size)}")

        with text_col:
            pasted_text = st.text_area(
                "Paste paragraph",
                key="pasted_text_input",
                height=150,
                placeholder="Paste a paragraph, notes, or article text here...",
            )

            use_pasted_text = st.button(
                "Use pasted text",
                use_container_width=True,
                disabled=not pasted_text.strip(),
            )

    return uploaded_file, pasted_text, use_pasted_text


def render_preview_tab(summary_type):
    text = st.session_state.uploaded_text

    if not text:
        st.markdown(
            """
            <div class="empty-state">
                Upload a file or paste text above to begin. The assistant will extract text,
                show document stats, and unlock summary, translation, audio, export, and chat.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown('<p class="section-kicker">Document preview</p>', unsafe_allow_html=True)
    st.text_area(
        "Extracted text",
        text[:6000],
        height=320,
        label_visibility="collapsed",
    )

    if len(text) > 6000:
        st.caption("Previewing the first 6,000 characters.")

    if st.session_state.tables:
        st.markdown("#### Tables found")
        for index, table in enumerate(st.session_state.tables, start=1):
            with st.expander(f"Table {index}", expanded=index == 1):
                st.dataframe(table, use_container_width=True)

    if st.button(
        "Generate summary",
        type="primary",
        use_container_width=True,
        disabled=not text.strip(),
    ):
        with st.spinner("Reading the document and composing a summary..."):
            summary = ai.summarize(text, summary_type)
            st.session_state.summary = summary
            st.session_state.translated_text = ""
            save_history(st.session_state.uploaded_filename, summary)
            index_document(text, st.session_state.uploaded_filename)

        st.toast("Summary generated and document indexed")
        st.rerun()


def render_summary_tab(language):
    summary = st.session_state.summary

    if not summary:
        st.markdown(
            """
            <div class="empty-state">
                Generate a summary from the Preview tab. Once it is ready, translation,
                audio playback, and export controls will appear here.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    st.markdown('<p class="section-kicker">AI summary</p>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="summary-box">{html.escape(summary)}</div>',
        unsafe_allow_html=True,
    )

    st.write("")
    action_col1, action_col2 = st.columns(2)

    with action_col1:
        if st.button("Translate summary", use_container_width=True):
            with st.spinner(f"Translating to {language}..."):
                st.session_state.translated_text = translate_text(summary, language)
            st.toast("Translation ready")

    with action_col2:
        if st.button("Create audio", use_container_width=True):
            with st.spinner("Generating audio..."):
                audio_file = text_to_speech(summary, language)
                with open(audio_file, "rb") as audio:
                    st.audio(audio.read(), format="audio/mp3")

    if st.session_state.translated_text:
        st.markdown("#### Translated summary")
        st.text_area(
            "Translated summary",
            st.session_state.translated_text,
            height=260,
            label_visibility="collapsed",
        )

    st.markdown("#### Export")
    export_col1, export_col2, export_col3 = st.columns(3)
    export_specs = [
        (export_col1, "PDF", "summary.pdf", "application/pdf"),
        (export_col2, "DOCX", "summary.docx", None),
        (export_col3, "TXT", "summary.txt", "text/plain"),
    ]

    for column, file_type, file_name, mime in export_specs:
        with column:
            if st.button(f"Prepare {file_type}", use_container_width=True):
                export_path = export_file(summary, file_type)
                with open(export_path, "rb") as file:
                    st.download_button(
                        f"Download {file_type}",
                        file,
                        file_name=file_name,
                        mime=mime,
                        use_container_width=True,
                    )


def render_chat_tab():
    if not is_document_indexed():
        st.markdown(
            """
            <div class="empty-state">
                Generate a summary first so the document can be indexed for question answering.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    question = st.chat_input("Ask a question about the indexed document")
    if question:
        with st.spinner("Searching the document..."):
            answer = chat_with_pdf(question)
        st.session_state.chat_history.append((question, answer))

    if not st.session_state.chat_history:
        st.info("Ask something specific, such as a definition, date, requirement, or conclusion.")
        return

    for question, answer in reversed(st.session_state.chat_history):
        st.markdown(
            f"""
            <div class="chat-row">
                <div class="chat-question">You asked: {html.escape(question)}</div>
                <div class="chat-answer">{html.escape(answer)}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )


def render_history_tab():
    try:
        history = load_history()
    except Exception:
        st.warning("Unable to load summary history.")
        return

    if not history:
        st.markdown(
            """
            <div class="empty-state">
                Previous summaries will appear here after your first generation.
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    for item in history[:20]:
        label = item["filename"]
        created_at = item.get("created_at")
        if created_at:
            label = f"{label} - {created_at}"

        with st.expander(label):
            st.write(item["summary"])


def render_footer():
    st.divider()
    st.caption(
        "Built with Python, Streamlit, Gemini, LangChain, FAISS, OCR, translation, and text-to-speech."
    )


create_database()
ensure_session_state()
inject_styles()
ai = load_model()

summary_type, language = render_sidebar()
render_hero()
uploaded_file, pasted_text, use_pasted_text = render_document_input()

if use_pasted_text:
    load_pasted_text(pasted_text)
    st.toast("Pasted text loaded")
    st.rerun()

if uploaded_file is not None and uploaded_file.name != st.session_state.uploaded_filename:
    try:
        with st.spinner("Extracting text and scanning document structure..."):
            load_uploaded_document(uploaded_file)
        st.toast("Document loaded")
    except Exception as exc:
        st.error(f"Could not load document: {exc}")

render_metrics(st.session_state.uploaded_text, st.session_state.summary)

preview_tab, summary_tab, chat_tab, history_tab = st.tabs(
    ["Preview", "Summary", "Chat", "History"]
)

with preview_tab:
    render_preview_tab(summary_type)

with summary_tab:
    render_summary_tab(language)

with chat_tab:
    render_chat_tab()

with history_tab:
    render_history_tab()

render_footer()
