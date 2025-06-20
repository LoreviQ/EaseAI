import os
import sys
import uuid
from datetime import datetime
from typing import List

import uvicorn
from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Add src to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from presentation_agent import PresentationAgent

# Initialize FastAPI app
app = FastAPI(
    title="PresentAI - AI Presentation Generator",
    description="Generate presentations using LangGraph AI agent with Google Gemini",
    version="1.0.0",
)

# Initialize templates - templates are now in src/templates
templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(__file__), "templates")
)

# Initialize the presentation agent
agent = PresentationAgent()

# Store generated presentations temporarily
presentation_store = {}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Serve the main demo page"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/generate-presentation")
async def generate_presentation(
    prompt: str = Form(...), files: List[UploadFile] = File(default=[])
):
    """Generate a presentation based on user prompt and uploaded files"""
    try:
        # Process uploaded files
        documents = []
        for file in files:
            if file.filename:
                content = await file.read()
                # For demo purposes, we'll assume text content
                # In production, you'd implement proper file parsing
                documents.append(
                    {
                        "filename": file.filename,
                        "content": content.decode("utf-8", errors="ignore"),
                        "content_type": file.content_type,
                    }
                )

        # Generate presentation using the agent
        result = agent.generate_presentation(user_prompt=prompt, documents=documents)

        if "error" in result:
            raise HTTPException(status_code=500, detail=result["error"])

        # Store the result with a unique ID
        presentation_id = str(uuid.uuid4())
        presentation_store[presentation_id] = result

        return {
            "presentation_id": presentation_id,
            "title": result.get("presentation_structure", {}).get(
                "title", "Generated Presentation"
            ),
            "slide_count": len(
                result.get("presentation_structure", {}).get("slides", [])
            ),
            "generated_at": result.get("generated_at"),
        }

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to generate presentation: {str(e)}"
        )


@app.get("/presentation/{presentation_id}")
async def get_presentation(presentation_id: str, request: Request):
    """View a generated presentation"""
    if presentation_id not in presentation_store:
        raise HTTPException(status_code=404, detail="Presentation not found")

    presentation = presentation_store[presentation_id]
    return templates.TemplateResponse(
        "presentation.html",
        {
            "request": request,
            "presentation": presentation,
            "presentation_id": presentation_id,
        },
    )


@app.get("/presentation/{presentation_id}/slides")
async def get_slides(presentation_id: str):
    """Get the HTML slides for a presentation"""
    if presentation_id not in presentation_store:
        raise HTTPException(status_code=404, detail="Presentation not found")

    presentation = presentation_store[presentation_id]
    return HTMLResponse(content=presentation.get("slides_html", ""))


@app.get("/presentation/{presentation_id}/notes")
async def get_speaker_notes(presentation_id: str):
    """Get speaker notes for a presentation"""
    if presentation_id not in presentation_store:
        raise HTTPException(status_code=404, detail="Presentation not found")

    presentation = presentation_store[presentation_id]
    return {
        "speaker_notes": presentation.get("speaker_notes", ""),
        "presentation_title": presentation.get("presentation_structure", {}).get(
            "title", ""
        ),
    }


@app.get("/presentation/{presentation_id}/script")
async def get_script(presentation_id: str):
    """Get the presentation script"""
    if presentation_id not in presentation_store:
        raise HTTPException(status_code=404, detail="Presentation not found")

    presentation = presentation_store[presentation_id]
    return {
        "script": presentation.get("script", ""),
        "presentation_title": presentation.get("presentation_structure", {}).get(
            "title", ""
        ),
    }


@app.get("/presentation/{presentation_id}/structure")
async def get_structure(presentation_id: str):
    """Get the presentation structure"""
    if presentation_id not in presentation_store:
        raise HTTPException(status_code=404, detail="Presentation not found")

    presentation = presentation_store[presentation_id]
    return presentation.get("presentation_structure", {})


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    uvicorn.run("src.main:app", host="0.0.0.0", port=8888, reload=True)
