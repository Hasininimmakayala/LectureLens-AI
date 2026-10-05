# 🎓 LectureLens AI

LectureLens AI is a local AI study assistant that turns lecture material into a searchable knowledge base.

## What it does

- Upload lecture PDFs
- Paste lecture notes
- Transcribe lecture audio with Whisper
- Extract text from board/slide images with OCR
- Split material into overlapping chunks
- Create semantic embeddings with Sentence Transformers
- Store/retrieve chunks with ChromaDB
- Answer questions using a local Ollama LLM
- Show the source files used for an answer
- Keep persistent chat history with SQLite
- Generate summaries, quiz questions, and revision notes

## Architecture

```text
PDF / Notes / Audio / Image
            ↓
      Text Extraction
            ↓
       Text Chunking
            ↓
 Sentence Transformer Embeddings
            ↓
         ChromaDB
            ↓
       Semantic Retrieval
            ↓
          Ollama
            ↓
       LectureLens Answer
```

## 1. Create the project

```bash
mkdir LectureLensAI
cd LectureLensAI
```

Put `app.py` and `requirements.txt` in this folder.

## 2. Create a virtual environment

Python 3.11 or 3.12 is recommended.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

If `python3.12` is not available, use your installed Python 3.11/3.12 command.

## 3. Install Python packages

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## 4. Install Ollama

Install Ollama, then pull a model. A lightweight option is:

```bash
ollama pull llama3.2:1b
```

Start Ollama if it is not already running:

```bash
ollama serve
```

Keep that terminal open.

You can check the model with:

```bash
ollama list
```

## 5. Optional Mac tools for audio and image OCR

For audio processing, FFmpeg is recommended:

```bash
brew install ffmpeg
```

For image OCR:

```bash
brew install tesseract
```

## 6. Run LectureLens

In another terminal, inside the project folder:

```bash
source .venv/bin/activate
streamlit run app.py
```

Streamlit will show a local URL, normally:

```text
http://localhost:8501
```

## 7. First demo

1. Open LectureLens in the browser.
2. Go to **Lecture PDF**.
3. Upload a lecture PDF.
4. Click **Process**.
5. Check the sidebar: the stored chunk count should increase.
6. Ask a question in **Ask LectureLens**.
7. The answer should appear with a **Sources** section.
8. Try **Summarize Lecture** or **Generate 5 Quiz Questions**.

## Important

LectureLens is designed to answer from uploaded material. If the relevant information is not in the knowledge base, it is instructed to say that it could not find the information instead of inventing an answer.

The folders/files `lecturelens_chroma/` and `lecturelens_chat.db` are generated automatically while the app runs and should normally be added to `.gitignore`.
