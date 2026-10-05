import os
import sqlite3
import uuid
from datetime import datetime

import streamlit as st
import ollama
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Optional features
try:
    from PIL import Image
    import pytesseract
    OCR_AVAILABLE = True
except Exception:
    OCR_AVAILABLE = False

st.set_page_config(page_title="LectureLens AI", page_icon="🎓", layout="wide")

APP_TITLE = "🎓 LectureLens AI"
DB_FILE = "lecturelens_fast.db"

# --------------------------------------------------
# DATABASE
# --------------------------------------------------
def db():
    return sqlite3.connect(DB_FILE, check_same_thread=False)


def init_db():
    conn = db()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            source TEXT NOT NULL,
            chunk_no INTEGER NOT NULL,
            content TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()


def add_chunks(source, chunks):
    conn = db()
    cur = conn.cursor()
    now = datetime.now().isoformat()
    for i, chunk in enumerate(chunks):
        cur.execute(
            "INSERT INTO chunks(source, chunk_no, content, created_at) VALUES (?, ?, ?, ?)",
            (source, i + 1, chunk, now),
        )
    conn.commit()
    conn.close()
    return len(chunks)


def get_chunks():
    conn = db()
    rows = conn.execute(
        "SELECT id, source, chunk_no, content FROM chunks ORDER BY id"
    ).fetchall()
    conn.close()
    return rows


def clear_database():
    conn = db()
    conn.execute("DELETE FROM chunks")
    conn.commit()
    conn.close()


init_db()

# --------------------------------------------------
# TEXT PROCESSING
# --------------------------------------------------
def split_text(text, size=800, overlap=120):
    text = " ".join(text.split())
    if not text:
        return []

    chunks = []
    start = 0
    step = max(1, size - overlap)
    while start < len(text):
        chunk = text[start:start + size].strip()
        if chunk:
            chunks.append(chunk)
        start += step
    return chunks


def extract_pdf(file):
    reader = PdfReader(file)
    pages = []
    for page in reader.pages:
        text = page.extract_text() or ""
        if text.strip():
            pages.append(text)
    return "\n".join(pages)


def retrieve(question, top_k=4):
    rows = get_chunks()
    if not rows:
        return []

    documents = [row[3] for row in rows]
    vectorizer = TfidfVectorizer(stop_words="english", ngram_range=(1, 2))
    matrix = vectorizer.fit_transform(documents)
    q_vector = vectorizer.transform([question])
    scores = cosine_similarity(q_vector, matrix).flatten()

    ranked = scores.argsort()[::-1]
    results = []
    for idx in ranked[:min(top_k, len(ranked))]:
        if scores[idx] <= 0:
            continue
        row = rows[idx]
        results.append({
            "source": row[1],
            "chunk": row[2],
            "content": row[3],
            "score": float(scores[idx]),
        })
    return results


def ollama_answer(question, contexts, model):
    if not contexts:
        return "I could not find this information in the uploaded lecture material."

    context_text = "\n\n".join(
        f"SOURCE: {x['source']} | CHUNK: {x['chunk']}\n{x['content']}"
        for x in contexts
    )

    prompt = f"""
You are LectureLens AI, a college lecture assistant.

Answer the student's question using ONLY the lecture material below.
Do not invent facts, dates, formulas, definitions, or examples.
If the answer is not present, clearly say that it was not found in the uploaded lecture material.
Keep the answer clear and student-friendly.

LECTURE MATERIAL:
{context_text}

STUDENT QUESTION:
{question}
"""

    response = ollama.chat(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response["message"]["content"]


def study_action(action, model):
    rows = get_chunks()
    if not rows:
        return "Please upload a lecture first."

    # Keep prompt size reasonable.
    material = "\n\n".join(r[3] for r in rows[:25])

    if action == "summary":
        instruction = "Create a concise lecture summary with headings and important points."
    elif action == "quiz":
        instruction = "Create 5 useful exam-style questions from the lecture and provide the answer after each question."
    else:
        instruction = "Create structured revision notes with definitions, key concepts, formulas if present, and important examples."

    prompt = f"""
You are LectureLens AI.
Use ONLY the lecture material below.
{instruction}
Do not invent information.

LECTURE MATERIAL:
{material}
"""
    response = ollama.chat(model=model, messages=[{"role": "user", "content": prompt}])
    return response["message"]["content"]


# --------------------------------------------------
# UI
# --------------------------------------------------
st.title(APP_TITLE)
st.caption("Upload lectures → retrieve relevant content → ask questions → study smarter")

with st.sidebar:
    st.header("⚙️ Settings")
    model = st.text_input("Ollama model", value="llama3.2:latest")
    top_k = st.slider("Retrieved chunks", 1, 8, 4)
    chunk_size = st.slider("Chunk size", 400, 1500, 800, 100)
    chunk_overlap = st.slider("Chunk overlap", 0, 300, 120, 20)

    st.divider()
    st.subheader("📚 Knowledge Base")
    count = len(get_chunks())
    st.metric("Stored chunks", count)

    if st.button("🗑️ Clear knowledge base", use_container_width=True):
        clear_database()
        st.success("Knowledge base cleared.")
        st.rerun()

# --------------------------------------------------
# INPUT TABS
# --------------------------------------------------
tab_pdf, tab_text, tab_image = st.tabs(["📄 Lecture PDF", "📝 Lecture Notes", "🖼️ Slide / Board Image"])

with tab_pdf:
    st.subheader("Upload lecture PDF")
    pdf = st.file_uploader("Choose a PDF", type=["pdf"], key="pdf")
    if pdf:
        if st.button("➕ Add PDF to LectureLens", key="add_pdf"):
            with st.spinner("Reading lecture PDF..."):
                text = extract_pdf(pdf)
            chunks = split_text(text, chunk_size, chunk_overlap)
            if chunks:
                n = add_chunks(pdf.name, chunks)
                st.success(f"Added {n} lecture chunks from {pdf.name}.")
            else:
                st.warning("No readable text was found. If this is a scanned PDF, use an OCR-enabled version.")

with tab_text:
    st.subheader("Paste lecture notes")
    title = st.text_input("Lecture title", placeholder="Example: Machine Learning - Unit 1")
    notes = st.text_area("Lecture notes", height=220, placeholder="Paste your lecture notes here...")
    if st.button("➕ Add Lecture Notes", key="add_notes"):
        if notes.strip():
            source = title.strip() or "Lecture Notes"
            chunks = split_text(notes, chunk_size, chunk_overlap)
            n = add_chunks(source, chunks)
            st.success(f"Added {n} chunks from {source}.")
        else:
            st.warning("Please enter lecture notes first.")

with tab_image:
    st.subheader("Upload a slide or board image")
    image_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"], key="image")
    if image_file:
        st.image(image_file, caption=image_file.name, use_container_width=True)
        if OCR_AVAILABLE:
            if st.button("🔎 Read image and add to knowledge base"):
                with st.spinner("Reading image text..."):
                    text = pytesseract.image_to_string(Image.open(image_file))
                chunks = split_text(text, chunk_size, chunk_overlap)
                if chunks:
                    n = add_chunks(image_file.name, chunks)
                    st.success(f"Added {n} OCR chunks.")
                else:
                    st.warning("No text was detected in the image.")
        else:
            st.info("OCR is not installed. You can still upload PDFs and paste notes.")

st.divider()

# --------------------------------------------------
# STUDY TOOLS
# --------------------------------------------------
st.header("🧠 Study Tools")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("📌 Summarize Lecture", use_container_width=True):
        with st.spinner("Creating summary..."):
            try:
                st.session_state.study_result = study_action("summary", model)
            except Exception as e:
                st.session_state.study_result = f"Ollama error: {e}"
with col2:
    if st.button("❓ Generate Quiz", use_container_width=True):
        with st.spinner("Creating quiz..."):
            try:
                st.session_state.study_result = study_action("quiz", model)
            except Exception as e:
                st.session_state.study_result = f"Ollama error: {e}"
with col3:
    if st.button("📝 Revision Notes", use_container_width=True):
        with st.spinner("Creating revision notes..."):
            try:
                st.session_state.study_result = study_action("revision", model)
            except Exception as e:
                st.session_state.study_result = f"Ollama error: {e}"

if "study_result" in st.session_state:
    st.markdown(st.session_state.study_result)

# --------------------------------------------------
# CHAT
# --------------------------------------------------
st.header("💬 Ask LectureLens")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask about your lecture...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        with st.spinner("Searching your lecture..."):
            contexts = retrieve(question, top_k)
        try:
            with st.spinner("LectureLens is thinking..."):
                answer = ollama_answer(question, contexts, model)
        except Exception as e:
            answer = (
                f"**Ollama connection error:** `{e}`\n\n"
                f"Make sure `{model}` is installed and Ollama is running."
            )
        st.markdown(answer)

        if contexts:
            st.markdown("### 📚 Sources")
            seen = set()
            for item in contexts:
                key = (item["source"], item["chunk"])
                if key not in seen:
                    st.write(f"• {item['source']} — chunk {item['chunk']}")
                    seen.add(key)

            with st.expander("🔍 View retrieved lecture content"):
                for item in contexts:
                    st.markdown(f"**{item['source']} — chunk {item['chunk']}**")
                    st.write(item["content"])
                    st.divider()

    st.session_state.messages.append({"role": "assistant", "content": answer})
