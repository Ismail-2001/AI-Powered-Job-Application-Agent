"""
FastAPI Server for AI Job Agent
Role: Expose the agentic workflow as a scalable API.
"""

import os
from typing import Dict, Any
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Import components
from utils.deepseek_client import DeepSeekClient
from utils.document_builder import DocumentBuilder
from utils.rag_engine import RAGEngine
from agents.job_analyzer import JobAnalyzer
from agents.cv_customizer import CVCustomizer
from agents.cover_letter_generator import CoverLetterGenerator

# Load config
load_dotenv()

app = FastAPI(title="AI Job Application Agent API")

# Add CORS middleware to allow requests from web interface
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize global engines
api_key = os.getenv("DEEPSEEK_API_KEY")
client = DeepSeekClient(api_key=api_key)
rag_engine = RAGEngine()
job_analyzer = JobAnalyzer(client)
cv_customizer = CVCustomizer(client)
cover_letter_generator = CoverLetterGenerator(client)
doc_builder = DocumentBuilder()

class JobRequest(BaseModel):
    job_description: str

@app.get("/")
async def root():
    return {"status": "online", "message": "Agentic AI Job Platform API is healthy"}

@app.post("/apply")
async def process_application(request: JobRequest):
    """
    End-to-end application workflow:
    Analysis -> RAG Retrieval -> Customization -> Generation
    """
    try:
        # 1. Analyze
        analysis = job_analyzer.analyze(request.job_description)
        
        # 2. RAG Retrieval (Strategic Improvement)
        keywords = analysis.get("keywords", {}).get("ats_keywords", [])
        relevant_snippets = rag_engine.retrieve_relevant_experience(keywords)
        
        # 3. Customize with RAG context
        # Load master profile for base info
        import json
        with open("data/master_profile.json", "r") as f:
            profile = json.load(f)
            
        customized_cv = cv_customizer.customize(profile, analysis, relevant_snippets)
        cover_letter = cover_letter_generator.generate(profile, analysis)

        # 4. Generate Files (In production these would go to S3, here we use 'output/')
        import re
        def sanitize(name): return re.sub(r'[<>:"/\\|?*]', '', str(name)).strip().replace(' ', '_')
        
        role = sanitize(analysis.get('role_info', {}).get('title', 'Job'))
        company = sanitize(analysis.get('role_info', {}).get('company', 'Company'))
        
        cv_path = f"output/API_CV_{company}_{role}.docx"
        cl_path = f"output/API_CL_{company}_{role}.docx"
        
        doc_builder.create_cv(customized_cv, cv_path)
        doc_builder.create_cover_letter(cover_letter, profile, cl_path)

        return {
            "success": True,
            "analysis": analysis,
            "files": {
                "cv": cv_path,
                "cover_letter": cl_path
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
