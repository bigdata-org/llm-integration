
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import json
import redis
import fitz 
from litellm import completion
import os
import uuid 
import markdownify
import logging  

# Load environment variables
load_dotenv()


app = FastAPI()

r = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")), 
    decode_responses=True,
    username="default",
    password=os.getenv("REDIS_PASSWORD"),
)
os.environ["GEMINI_API_KEY"] = os.getenv("GEMINI_API_KEY")


# Enable logging
logging.basicConfig(level=logging.INFO)

def parse_pdf_to_markdown(pdf_content: bytes) -> str:
    content = ""
    with fitz.open(stream=pdf_content, filetype='pdf') as doc:
        for page in doc:
            page_text = page.get_text("html")
            content += f"\n## Page {page.number + 1}\n" + markdownify.markdownify(page_text)
    return content

# Endpoint to upload and store PDF content in Markdown format
@app.post("/upload_pdf")
async def upload_pdf(file: UploadFile = File(...)):
    try:
        markdown_content = parse_pdf_to_markdown(await file.read())

        document_id = f"{file.filename}_{uuid.uuid4().hex}" 
        r.set(f"document:{document_id}:markdown", markdown_content)

        parsed_pdfs = json.loads(r.get("parsed_pdfs") or "[]")
        if document_id not in parsed_pdfs:
            parsed_pdfs.append(document_id)
        r.set("parsed_pdfs", json.dumps(parsed_pdfs))

        logging.info(f"Document '{document_id}' uploaded successfully.")
        return JSONResponse(content={"document_id": document_id})

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to select previously parsed PDF content
@app.get("/select_pdfcontent")
async def select_pdfcontent():
    parsed_pdfs = json.loads(r.get("parsed_pdfs") or "[]")
    return JSONResponse(content={"parsed_pdfs": parsed_pdfs})



@app.post("/summarize")
async def summarize(document_id: str = Form(...)):
    try:
        # Retrieve the markdown content for the document
        markdown_content = r.get(f"document:{document_id}:markdown")
        
        if not markdown_content:
            raise HTTPException(status_code=404, detail="Document not found")

        # Construct prompt for summarization
        prompt = f"Summarize the following document:\n{markdown_content[:3000]}..."  

        # Call Gemini API for summary
        response = completion(
            model="gemini/gemini-1.5-pro",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000,
            api_key=os.getenv("GEMINI_API_KEY")
        )

        # Return the summary
        summary = response.choices[0].message.content
        return JSONResponse(content={"summary": summary})

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))


# Endpoint to ask questions about PDFs
@app.post("/ask_question")
async def ask_question(document_id: str = Form(...), question: str = Form(...)):
    try:
        markdown_content = r.get(f"document:{document_id}:markdown")
        if not markdown_content:
            raise HTTPException(status_code=404, detail="Document not found")

        prompt = (
            f"Answer the following question based on the document:\n"
            f"{markdown_content[:3000]}...\n"
            f"Question: {question}\n"
            f"Include key points from tables, charts, and images if relevant."
        )
        response = completion(
            model="gemini/gemini-1.5-pro",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=1000,
            api_key=os.getenv("GEMINI_API_KEY")
        )
        answer = response.choices[0].message.content

        return JSONResponse(content={"answer": answer})

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))






