# HR Resource Query Chatbot

![Chatbot Demo](https://i.imgur.com/7bQyX5G.png)

## Overview
This project is an intelligent HR assistant chatbot designed to help managers and HR teams find suitable employees for projects based on natural language queries. It leverages a Retrieval-Augmented Generation (RAG) system to understand user requests and provide insightful, context-aware recommendations.

The application uses a hybrid AI approach, performing semantic search locally and using a cloud-based LLM for generation. It is built with a **FastAPI** backend and a **Streamlit** frontend.

## Features
- **Natural Language Understanding**: Ask complex questions like "Who has worked on healthcare projects?"
- **Hybrid RAG Pipeline**:
  - **Retrieval**: Uses a local `Sentence-Transformers` model and `FAISS` vector search to find relevant employees semantically and instantly. This process is fast, free, and private.
  - **Generation**: Leverages **Google's Gemini API** (via the free tier) to generate high-quality, synthesized responses.
- **RESTful API**: A robust FastAPI backend provides endpoints for chat and structured search.
- **Interactive UI**: A clean and simple chat interface built with Streamlit.

## Architecture
The system consists of three main components:

1.  **Frontend (Streamlit)**: A lightweight web interface that captures user queries and displays the generated responses.
2.  **Backend (FastAPI)**: The application's core. It exposes REST endpoints and orchestrates the RAG pipeline.
3.  **RAG System (AI/ML Core)**:
    - **Data Loader**: Loads employee data from `employees.json`.
    - **Vector Store**: On startup, employee profiles are converted into vector embeddings using a local `SentenceTransformer` model and indexed in-memory using `FAISS`.
    - **LLM Service**: Interacts with the Google Gemini API to generate the final response based on the retrieved context.

**Flow Diagram:**
`User Query (Streamlit) -> POST Request -> FastAPI Backend -> RAG System (Local Retrieve -> Augment -> Cloud Generate) -> Google Gemini API -> Response -> Streamlit UI`

## Setup & Installation
**Prerequisites:**
- Python 3.8+
- A Google Gemini API Key

**Instructions:**
1.  Clone the repository.
2.  Create and activate a Python virtual environment.
3.  Install dependencies: `pip install -r requirements.txt`
4.  Create a `.env` file and add your API key: `GOOGLE_API_KEY="your_api_key_here"`
5.  Run the backend: `uvicorn app.main:app --reload`
6.  In a separate terminal, run the frontend: `streamlit run app/frontend.py`

## Technical Decisions
- **Hybrid AI Model**: We chose a hybrid approach to balance performance, cost, and privacy.
  - **Local Embeddings** (`Sentence-Transformers`): Retrieval is a high-frequency task. Running it locally makes it free, instant, and ensures employee data used for searching never leaves the machine.
  - **Cloud Generation** (`Google Gemini API`): Generation requires a powerful LLM. Using the Gemini API's free tier gives us state-of-the-art text generation without needing a powerful local GPU.
- **FAISS vs. Vector Database**: For this project's scale, an in-memory library like `FAISS` is highly efficient and avoids the operational overhead of a dedicated database service.