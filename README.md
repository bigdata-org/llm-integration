# llm-integration
Integratig llm with pdf scrapper

### Api url : https://case-798800248787.us-central1.run.app
### Streamlit url: https://frontend-gpt-qyjhl6rcsnihsnsm723eaq.streamlit.app/

#Overview
This project enhances the existing assignment by developing a **Streamlit application** that integrates **Large Language Models (LLMs)** using **FastAPI** and **LiteLLM** for API management. The application allows users to summarize and answer questions based on uploaded PDF documents.

## Objectives

### 1. Streamlit Front-End
- Build a user-friendly interface with the following features:
  - Select previously parsed PDF content or upload new PDF files.
  - Use LLMs (e.g., GPT-4o) via LiteLLM to:
    - Provide summaries of document content.
    - Answer user-submitted questions about the document.
  - Include options for:
    - Selecting an LLM.
    - File upload and text input for questions.
    - Buttons to trigger summarization and Q&A functionalities.
    - Display areas for generated summaries and answers.

### 2. FastAPI Back-End
- Set up REST API endpoints to handle interactions with the Streamlit front-end:
  - `/select_pdfcontent`: Select prior parsed content.
  - `/upload_pdf`: Upload new PDF files.
  - `/summarize`: Generate summaries of documents.
  - `/ask_question`: Process user questions and return answers.
- Use Redis streams for communication between services.
- Ensure proper response formats (JSON) and implement error handling.

### 3. LiteLLM Integration
- Manage interactions with various LLM APIs using LiteLLM.
- Document token usage (input/output) for each query.
- Implement error handling and logging for API calls.

### 4. Deployment
- Deploy all components using Docker Compose on the cloud.

## Deliverables

1. **GitHub Repository**
   - Well-organized, documented, and structured codebase.
   - A detailed `README.md` file with setup instructions.
   - Diagrammatic representations of architecture and data flows.

2. **Documentation**
   - `AIUseDisclosure.md`: Transparently list all AI tools used and their specific applications in the project.
   - Technical and architectural diagrams illustrating processing flows.

3. **Submission Details**
   - Task tracking using GitHub issues.
   - A final, detailed Codelab outlining step-by-step implementation.

## Supported LLM Models
- **OpenAI GPT-4o**: [Documentation](#)
- **Google Gemini 2.0 Flash**: [Documentation](#)
- **DeepSeek**: [Documentation](#)
- **Anthropic Claude**: [Documentation](#)
