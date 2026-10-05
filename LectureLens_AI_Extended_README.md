# 🎓 LectureLens AI

LectureLens AI is a local AI-powered study assistant designed to help students learn from their own lecture material.

Instead of manually searching through long lecture PDFs, notes, recordings, and slide or board images, students can add their study material to LectureLens and interact with it using natural-language questions.

The application combines **Retrieval-Augmented Generation (RAG)** with **Ollama and Llama 3.2** to retrieve relevant lecture information and generate clear, context-aware answers locally.

---

## 📚 What LectureLens AI Can Do

LectureLens is designed around the way students actually study.

### 📄 Lecture PDFs

- Upload lecture PDFs
- Extract text from the document
- Split the content into manageable chunks
- Create embeddings for semantic search
- Store the content in ChromaDB
- Retrieve relevant sections when answering questions

### 📝 Lecture Notes

Students can paste their own lecture notes directly into the application.

The notes are processed and added to the same knowledge base, so information from notes can be used together with uploaded PDFs.

### 🎧 Lecture Audio

LectureLens can process lecture recordings using **Whisper / faster-whisper**.

The workflow is:

```text
Lecture Audio
      ↓
Whisper Transcription
      ↓
Generated Transcript
      ↓
Text Chunking
      ↓
Embeddings
      ↓
ChromaDB
```

This makes recorded lectures searchable without manually typing the entire lecture.

### 🖼️ Board and Slide Images

Students can upload images such as:

- Classroom board photographs
- Lecture slide screenshots
- Scanned notes
- Other lecture-related images

OCR is used to extract readable text from the image before adding it to the knowledge base.

### 💬 Ask LectureLens

Students can ask questions about their uploaded material.

For example:

```text
What is the main concept explained in this lecture?
```

```text
Explain the second topic in simple words.
```

```text
What are the advantages discussed in the lecture?
```

LectureLens retrieves relevant content first and then sends that context to the local LLM.

### 📌 Summarize Lectures

LectureLens can generate a summary of the available lecture material so students can quickly review the important concepts.

### ❓ Generate Quiz Questions

Students can generate quiz questions from their lecture content for self-practice and exam preparation.

Example:

```text
Generate 5 quiz questions from this lecture.
```

### 📝 Revision Notes

LectureLens can also create revision-friendly notes from the stored lecture content.

This can be useful before tests and examinations.

### 💾 Persistent Chat History

Chat history can be stored using SQLite so students can continue working with previous conversations instead of starting from zero every time.

### 🔎 Source-Aware Answers

When possible, LectureLens keeps track of the source material used for retrieval, making it easier to understand where an answer came from.

---

# 🧠 How LectureLens Works

LectureLens follows a Retrieval-Augmented Generation architecture.

```text
        Lecture Material
              │
      ┌───────┼────────┐
      ↓       ↓        ↓
     PDF     Notes    Audio/Image
      │       │        │
      └───────┼────────┘
              ↓
        Text Extraction
              ↓
          Text Cleaning
              ↓
           Chunking
              ↓
   Sentence Transformer
        Embeddings
              ↓
           ChromaDB
              ↓
      Semantic Retrieval
              ↓
       Relevant Context
              ↓
        Ollama + Llama 3.2
              ↓
       LectureLens Answer
```

When a student asks a question, the application does not simply send the question to the LLM.

Instead, it:

1. Receives the student's question.
2. Searches the LectureLens knowledge base.
3. Retrieves the most relevant lecture chunks.
4. Builds a context from those chunks.
5. Sends the retrieved context and question to Ollama.
6. Generates an answer based on the available lecture information.
7. Displays the response and relevant sources.

This approach helps keep answers focused on the student's actual study material.

---

# 🛠️ Technology Stack

| Technology | Purpose |
|---|---|
| **Python** | Main programming language |
| **Streamlit** | Web application interface |
| **PyPDF** | Extract text from lecture PDFs |
| **Sentence Transformers** | Generate semantic text embeddings |
| **ChromaDB** | Store and retrieve document embeddings |
| **Ollama** | Run the LLM locally |
| **Llama 3.2** | Generate natural-language responses |
| **Whisper / faster-whisper** | Transcribe lecture audio |
| **Pytesseract** | OCR for lecture images |
| **Pillow** | Image processing |
| **SQLite** | Persistent chat history |

---

# 🔄 RAG Pipeline

The main RAG pipeline can be summarized as:

```text
Document
   ↓
Text Extraction
   ↓
Text Cleaning
   ↓
Chunking
   ↓
Embedding Generation
   ↓
Vector Storage
   ↓
Question
   ↓
Semantic Retrieval
   ↓
Relevant Context
   ↓
Local LLM
   ↓
Answer
```

The important idea is that the LLM receives relevant information retrieved from the lecture knowledge base instead of relying only on its general training knowledge.

---

# ✨ Main Features

- 📄 Upload lecture PDFs
- 📝 Add lecture notes
- 🎧 Transcribe lecture recordings
- 🖼️ Extract text from board and slide images
- 🔍 Semantic retrieval from lecture material
- 💬 Ask questions about lectures
- 📌 Generate summaries
- ❓ Generate quiz questions
- 📝 Generate revision notes
- 📚 Store multiple lecture sources
- 🔎 Display source information
- 💾 Maintain chat history
- 🤖 Run the language model locally
- 🔐 No paid LLM API required

---

# 🚀 Getting Started

## 1. Clone the Repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd LectureLens-AI
```

---

## 2. Create a Virtual Environment

Python **3.11 or 3.12** is recommended.

```bash
python3.12 -m venv .venv
```

Activate the environment:

```bash
source .venv/bin/activate
```

If your system uses Python 3.11:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

---

## 3. Upgrade pip

```bash
pip install --upgrade pip
```

---

## 4. Install Python Dependencies

```bash
pip install -r requirements.txt
```

The requirements include the libraries needed for PDF processing, embeddings, ChromaDB, Streamlit, Ollama, OCR, and audio processing.

---

# 🤖 Setting Up Ollama

LectureLens uses Ollama to run the language model locally.

Install Ollama first, then download the model.

```bash
ollama pull llama3.2
```

Check that the model is installed:

```bash
ollama list
```

You should see your Llama 3.2 model in the list.

If Ollama is not already running, start it with:

```bash
ollama serve
```

Keep the Ollama process running while using LectureLens.

---

# 🎧 Optional Audio Setup

For lecture audio processing, FFmpeg is recommended.

On macOS:

```bash
brew install ffmpeg
```

LectureLens uses Whisper / faster-whisper to convert lecture recordings into text.

The first transcription can take longer because the Whisper model may need to be downloaded.

---

# 🖼️ Optional OCR Setup

For extracting text from lecture images, install Tesseract on macOS:

```bash
brew install tesseract
```

The Python OCR package can be installed through the project requirements.

---

# ▶️ Run LectureLens

Activate your virtual environment:

```bash
source .venv/bin/activate
```

Then run:

```bash
streamlit run app.py
```

Streamlit normally opens the application at:

```text
http://localhost:8501
```

---

# 🧪 First Demo

After starting the application:

### Step 1
Open LectureLens in your browser.

### Step 2
Upload a lecture PDF.

### Step 3
Process the lecture material.

### Step 4
Ask a question about the uploaded lecture.

For example:

```text
Explain the main topic of this lecture.
```

### Step 5
Check the generated answer and its source information.

### Step 6
Try the other study tools:

- Summarize Lecture
- Generate Quiz Questions
- Generate Revision Notes

### Step 7
Try adding lecture notes, an audio recording, or an image of lecture slides/board notes.

---

# 📁 Project Structure

A typical project structure looks like this:

```text
LectureLens-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── .venv/
│
├── lecturelens_chroma/
│
└── lecturelens_chat.db
```

The `.venv` folder is the Python virtual environment.

The ChromaDB and SQLite files are generated while the application runs.

These generated files should normally not be committed to GitHub.

---

# 🔐 Local and Privacy-Friendly Design

One of the main goals of LectureLens is to keep the study workflow local.

The application is designed to use:

```text
Student Material
      ↓
Local Processing
      ↓
Local Vector Database
      ↓
Local Ollama Model
      ↓
Answer
```

No paid cloud LLM API is required for the core question-answering workflow.

This makes the project useful for students who want to experiment with AI while keeping their lecture material on their own computer.

---

# 🎯 Project Goal

The goal of LectureLens AI is to create a practical AI study assistant that works with the material students already use.

Instead of switching between PDF readers, notes, recorded lectures, and separate AI tools, students can bring their lecture resources into one application.

LectureLens is intended to help students:

- Understand difficult concepts
- Search through lecture material
- Review long lectures quickly
- Create revision notes
- Practice using quizzes
- Ask follow-up questions
- Learn from recorded lectures
- Prepare for examinations

---

# 💡 Why RAG?

A normal LLM may not know the specific content of a student's lecture.

For example, a professor may explain a topic using a particular definition, example, diagram, or set of notes.

RAG allows LectureLens to first retrieve information from the student's uploaded material and then use that information when generating the answer.

```text
Student Question
       ↓
Search Lecture Knowledge Base
       ↓
Retrieve Relevant Information
       ↓
Send Context to LLM
       ↓
Generate Answer
```

This makes the application more useful for document-based question answering.

---

# 📈 Future Improvements

Possible future improvements include:

- 📑 Page-level source citations
- 🎯 Better semantic retrieval
- 📊 Retrieval and answer evaluation
- 🧠 Improved conversation memory
- 🗂️ Separate knowledge bases for different subjects
- 📚 Multiple course management
- 📝 Automatic exam preparation
- 🎴 Flashcard generation
- 📊 Learning progress tracking
- 🌐 Support for additional document formats
- 🎙️ Improved lecture transcription
- 🖼️ Better handling of diagrams and images

---

# ⚠️ Important

LectureLens is designed to answer questions using the uploaded lecture material.

If the required information is not available in the knowledge base, the application should indicate that the information could not be found rather than inventing lecture-specific details.

Generated information should still be reviewed by the student, especially when preparing for examinations.

---

# 👩‍💻 Author

**Hasini Nimmakayala**

B.Tech – Computer Science and Engineering

---

# ⭐ Acknowledgement

LectureLens AI was developed as a learning project to explore practical applications of:

- Retrieval-Augmented Generation
- Local Large Language Models
- Vector databases
- Semantic search
- Speech-to-text
- OCR
- Generative AI
- AI-assisted education

