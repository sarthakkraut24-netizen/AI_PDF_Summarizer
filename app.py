# ==========================================================
# AI DOCUMENT ASSISTANT
# app.py - Part 1
# Compatible with Python 3.13+
# ==========================================================

import os
from datetime import datetime

import streamlit as st

from summarizer import AISummarizer
from file_reader import read_file
from translator import translate_text, LANGUAGES
from tts import text_to_speech

from utils import (
    word_count,
    character_count,
    sentence_count,
    paragraph_count,
    reading_time,
    compression_percentage,
    save_summary,
    save_history,
    load_history,
    project_info
)

from database import (
    init_db,
    save_summary_db,
    get_history,
    total_summaries,
    database_stats
)

from pdf_chat import (
    create_vector_database,
    load_chatbot,
    ask_question
)

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="AI Document Assistant",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

init_db()

# ==========================================================
# LOAD AI MODEL
# ==========================================================

@st.cache_resource
def load_model():

    return AISummarizer()

ai = load_model()

# ==========================================================
# SESSION STATE
# ==========================================================

if "summary" not in st.session_state:

    st.session_state.summary = ""

if "translated_summary" not in st.session_state:

    st.session_state.translated_summary = ""

if "pdf_chatbot" not in st.session_state:

    st.session_state.pdf_chatbot = None

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.main{
    background:#f5f7fa;
}

.block-container{
    padding-top:2rem;
    padding-bottom:2rem;
}

div[data-testid="metric-container"]{
    background:white;
    border-radius:15px;
    padding:18px;
    border:1px solid #E5E7EB;
}

.stButton>button{
    width:100%;
    height:48px;
    border-radius:12px;
    font-size:16px;
    font-weight:bold;
}

textarea{
    border-radius:10px !important;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# TITLE
# ==========================================================

st.title("🤖 AI Document Assistant")

st.caption(
    "Summarize • Translate • Chat with PDF • Text-to-Speech"
)

# ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.header("📊 Dashboard")

    stats = database_stats()

    st.metric(
        "Total Summaries",
        stats["Total Summaries"]
    )

    st.metric(
        "Total Words",
        stats["Total Words"]
    )

    st.divider()

    st.subheader("⚙️ Settings")

    summary_type = st.selectbox(
        "Summary Length",
        [
            "Short",
            "Medium",
            "Long"
        ]
    )

    language = st.selectbox(
        "Translate Summary",
        list(LANGUAGES.keys())
    )

    st.divider()

    st.subheader("ℹ️ Project Information")

    info = project_info()

    st.write(f"**Project:** {info['Project']}")
    st.write(f"**Version:** {info['Version']}")
    st.write(f"**Framework:** {info['Framework']}")
    st.write(f"**Database:** {info['Database']}")
    st.write(f"**AI Model:** {info['AI Model']}")
    st.write(f"**Chat Model:** {info['Chat Model']}")
# ==========================================================
# FILE UPLOAD
# ==========================================================

st.divider()

st.header("📄 Upload Document")

uploaded_file = st.file_uploader(
    "Choose a PDF, DOCX or TXT file",
    type=["pdf", "docx", "txt"]
)

st.markdown("### OR")

manual_text = st.text_area(
    "✍️ Paste your text here",
    height=250,
    placeholder="Enter or paste your text..."
)

# ==========================================================
# READ INPUT TEXT
# ==========================================================

text = ""

if uploaded_file is not None:

    try:

        text = read_file(uploaded_file)

    except Exception as e:

        st.error(f"Error reading file: {e}")

elif manual_text.strip():

    text = manual_text.strip()

# ==========================================================
# GENERATE SUMMARY
# ==========================================================

if st.button("🚀 Generate AI Summary", use_container_width=True):

    if not text:

        st.warning("Please upload a file or paste some text.")

    else:

        with st.spinner("Generating AI Summary..."):

            summary = ai.summarize(
                text,
                summary_type
            )

            st.session_state.summary = summary

            if language == "English":

                translated = summary

            else:

                translated = translate_text(
                    summary,
                    language
                )

            st.session_state.translated_summary = translated

            save_summary(summary)

            save_history(
                text,
                summary
            )

            filename = "Manual Input"

            if uploaded_file is not None:

                filename = uploaded_file.name

            save_summary_db(

                filename=filename,

                summary_type=summary_type,

                language=language,

                original_text=text,

                summary=summary

            )

            if (
                uploaded_file is not None
                and uploaded_file.name.lower().endswith(".pdf")
            ):

                os.makedirs(
                    "uploads",
                    exist_ok=True
                )

                pdf_path = os.path.join(
                    "uploads",
                    uploaded_file.name
                )

                with open(pdf_path, "wb") as file:

                    file.write(
                        uploaded_file.getbuffer()
                    )

                try:

                    create_vector_database(
                        pdf_path
                    )

                    st.session_state.pdf_chatbot = load_chatbot()

                    st.success(
                        "📚 PDF Chatbot Ready!"
                    )

                except Exception as e:

                    st.warning(
                        f"PDF Chat could not be initialized.\n{e}"
                    )

        st.success("✅ Summary Generated Successfully!")
# ==========================================================
# DISPLAY RESULTS
# ==========================================================

st.divider()

tab1, tab2, tab3 = st.tabs(
    [
        "📄 Original Text",
        "🤖 AI Summary",
        "🌍 Translation"
    ]
)

# ==========================================================
# ORIGINAL TEXT
# ==========================================================

with tab1:

    st.text_area(
        "Original Text",
        value=text,
        height=400,
        disabled=True
    )

# ==========================================================
# SUMMARY
# ==========================================================

with tab2:

    if st.session_state.summary:

        st.text_area(
            "Generated Summary",
            value=st.session_state.summary,
            height=400,
            disabled=True
        )

    else:

        st.info(
            "Generate a summary to view it here."
        )

# ==========================================================
# TRANSLATION
# ==========================================================

with tab3:

    if st.session_state.translated_summary:

        st.text_area(
            "Translated Summary",
            value=st.session_state.translated_summary,
            height=400,
            disabled=True
        )

    else:

        st.info(
            "No translated summary available."
        )

# ==========================================================
# DOCUMENT STATISTICS
# ==========================================================

st.divider()

st.subheader("📊 Document Statistics")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Words",
    word_count(text)
)

col2.metric(
    "Characters",
    character_count(text)
)

col3.metric(
    "Sentences",
    sentence_count(text)
)

col4.metric(
    "Paragraphs",
    paragraph_count(text)
)

st.divider()

col5, col6 = st.columns(2)

col5.metric(
    "Reading Time",
    f"{reading_time(text)} min"
)

col6.metric(
    "Compression",
    f"{compression_percentage(text, st.session_state.summary)}%"
)

# ==========================================================
# TEXT TO SPEECH
# ==========================================================

if st.session_state.summary:

    st.divider()

    st.subheader("🔊 Listen to Summary")

    audio_name = (
        f"summary_"
        f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp3"
    )

    audio_file = text_to_speech(

        st.session_state.summary,

        filename=audio_name,

        language=language

    )

    if audio_file:

        with open(audio_file, "rb") as audio:

            st.audio(audio.read())

# ==========================================================
# DOWNLOAD SUMMARY
# ==========================================================

if st.session_state.summary:

    st.download_button(

        label="📥 Download Summary",

        data=st.session_state.summary,

        file_name="summary.txt",

        mime="text/plain",

        use_container_width=True

    )
# ==========================================================
# CHAT WITH PDF
# ==========================================================

st.divider()

st.header("💬 Chat with PDF")

if st.session_state.pdf_chatbot is not None:

    question = st.text_input(
        "Ask a question about your uploaded PDF",
        placeholder="Example: What is the conclusion of this document?"
    )

    if st.button("🤖 Ask AI", use_container_width=True):

        if question.strip():

            with st.spinner("Searching document..."):

                try:

                    answer = ask_question(
                        st.session_state.pdf_chatbot,
                        question
                    )

                    st.success("Answer")

                    st.write(answer)

                except Exception as e:

                    st.error(f"Error: {e}")

        else:

            st.warning("Please enter a question.")

else:

    st.info(
        "Upload a PDF and generate a summary to activate the PDF chatbot."
    )

# ==========================================================
# SUMMARY HISTORY
# ==========================================================

st.divider()

st.header("📚 Summary History")

history = get_history()

if history:

    for item in history:

        with st.expander(
            f"📄 {item[1]} | {item[6]}"
        ):

            st.write("### File Name")

            st.write(item[1])

            st.write("### Summary Type")

            st.write(item[2])

            st.write("### Language")

            st.write(item[3])

            st.write("### Summary")

            st.write(item[5])

else:

    st.info("No summaries found in the database.")

# ==========================================================
# HISTORY FILE
# ==========================================================

st.divider()

st.header("📝 Saved History")

history_text = load_history()

st.text_area(

    "History",

    value=history_text,

    height=250,

    disabled=True

)

# ==========================================================
# DASHBOARD
# ==========================================================

st.divider()

st.header("📊 Dashboard")

stats = database_stats()

col1, col2 = st.columns(2)

col1.metric(

    "Total Summaries",

    stats["Total Summaries"]

)

col2.metric(

    "Total Words",

    stats["Total Words"]

)

# ==========================================================
# PROJECT INFORMATION
# ==========================================================

st.divider()

st.header("ℹ️ Project Information")

info = project_info()

col1, col2 = st.columns(2)

with col1:

    st.write(f"**Project:** {info['Project']}")

    st.write(f"**Version:** {info['Version']}")

    st.write(f"**Framework:** {info['Framework']}")

with col2:

    st.write(f"**Language:** {info['Language']}")

    st.write(f"**Database:** {info['Database']}")

    st.write(f"**AI Model:** {info['AI Model']}")

    st.write(f"**Chat Model:** {info['Chat Model']}")
# ==========================================================
# FINAL SETTINGS
# ==========================================================

st.divider()

st.subheader("⚙️ Application Settings")

auto_clear = st.checkbox(
    "Clear input after generating summary",
    value=False
)

show_success = st.checkbox(
    "Show success messages",
    value=True
)

# ==========================================================
# SESSION CLEANUP
# ==========================================================

if auto_clear:

    if st.button("🗑 Clear Current Session"):

        st.session_state.summary = ""

        st.session_state.translated_summary = ""

        st.session_state.pdf_chatbot = None

        st.rerun()

# ==========================================================
# SYSTEM STATUS
# ==========================================================

st.divider()

st.subheader("🖥 System Status")

status_col1, status_col2, status_col3 = st.columns(3)

status_col1.success("✅ AI Model Loaded")

status_col2.success("✅ Database Connected")

if st.session_state.pdf_chatbot:

    status_col3.success("✅ PDF Chat Ready")

else:

    status_col3.info("Waiting for PDF Upload")

# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.markdown(
    """
    <div style="text-align:center;padding:20px;">
        <h3>🤖 AI Document Assistant</h3>
        <p>
            Built with ❤️ using
            <b>Python 3.13</b>,
            <b>Streamlit</b>,
            <b>Transformers</b>,
            <b>Google Gemini</b>,
            <b>FAISS</b>,
            <b>SQLite</b>
        </p>
        <p>
            © 2026 Sarthak Raut
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# ==========================================================
# FINAL SUCCESS MESSAGE
# ==========================================================

if show_success:

    st.success("🎉 AI Document Assistant is running successfully!")