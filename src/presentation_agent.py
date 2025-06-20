import json
import os
from datetime import datetime
from typing import Dict, List, Optional, TypedDict

import markdown
from dotenv import load_dotenv
from langchain.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.graph import END, StateGraph

# Load environment variables
load_dotenv()


class PresentationState(TypedDict):
    """State for the presentation generation workflow"""

    user_prompt: str
    documents: List[Dict]
    document_content: str
    presentation_structure: Dict
    slides_html: str
    speaker_notes: str
    script: str
    error: str


class PresentationAgent:
    def __init__(self):
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            temperature=0.7,
            google_api_key=os.getenv("GOOGLE_API_KEY"),
        )
        self.workflow = self._create_workflow()

    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow for presentation generation"""
        workflow = StateGraph(PresentationState)

        # Add nodes
        workflow.add_node("process_documents", self._process_documents)
        workflow.add_node("create_structure", self._create_structure)
        workflow.add_node("generate_slides", self._generate_slides)
        workflow.add_node("generate_notes", self._generate_notes)
        workflow.add_node("generate_script", self._generate_script)

        # Add edges
        workflow.set_entry_point("process_documents")
        workflow.add_edge("process_documents", "create_structure")
        workflow.add_edge("create_structure", "generate_slides")
        workflow.add_edge("generate_slides", "generate_notes")
        workflow.add_edge("generate_notes", "generate_script")
        workflow.add_edge("generate_script", END)

        return workflow.compile()

    def _process_documents(self, state: PresentationState) -> PresentationState:
        """Process uploaded documents and extract content"""
        try:
            document_content = ""

            for doc in state.get("documents", []):
                content = self._extract_document_content(doc)
                document_content += (
                    f"\n\n--- Document: {doc.get('filename', 'Unknown')} ---\n{content}"
                )

            state["document_content"] = document_content
            return state
        except Exception as e:
            state["error"] = f"Error processing documents: {str(e)}"
            return state

    def _extract_document_content(self, document: Dict) -> str:
        """Extract content from different document types"""
        filename = document.get("filename", "").lower()
        content = document.get("content", "")

        if filename.endswith(".pdf"):
            return self._extract_pdf_content(content)
        elif filename.endswith((".docx", ".doc")):
            return self._extract_docx_content(content)
        elif filename.endswith((".xlsx", ".xls")):
            return self._extract_excel_content(content)
        elif filename.endswith(".txt"):
            return content
        elif filename.endswith(".md"):
            return markdown.markdown(content)
        else:
            return content

    def _extract_pdf_content(self, content: str) -> str:
        """Extract text from PDF content"""
        try:
            # For demo purposes, assuming content is already extracted
            return content
        except Exception as e:
            return f"Error extracting PDF content: {str(e)}"

    def _extract_docx_content(self, content: str) -> str:
        """Extract text from DOCX content"""
        try:
            # For demo purposes, assuming content is already extracted
            return content
        except Exception as e:
            return f"Error extracting DOCX content: {str(e)}"

    def _extract_excel_content(self, content: str) -> str:
        """Extract text from Excel content"""
        try:
            # For demo purposes, assuming content is already extracted
            return content
        except Exception as e:
            return f"Error extracting Excel content: {str(e)}"

    def _create_structure(self, state: PresentationState) -> PresentationState:
        """Create the presentation structure based on prompt and documents"""
        try:
            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are an expert presentation designer. Create a comprehensive presentation structure based on the user's prompt and supporting documents.

Your task is to analyze the content and create a well-organized presentation structure with:
1. A compelling title
2. 5-8 slides with clear titles and key points
3. Logical flow and storytelling
4. Engaging content that matches the audience and purpose

Return your response as a JSON object with this structure:
{
    "title": "Presentation Title",
    "slides": [
        {
            "slide_number": 1,
            "title": "Slide Title",
            "type": "title_slide|content|conclusion",
            "key_points": ["Point 1", "Point 2", "Point 3"],
            "speaker_notes_outline": "Brief outline for speaker notes"
        }
    ],
    "target_audience": "Description of target audience",
    "presentation_style": "professional|casual|academic|creative"
}""",
                    ),
                    (
                        "human",
                        f"""Create a presentation structure for:

User Prompt: {state["user_prompt"]}

Supporting Documents Content:
{state.get("document_content", "No documents provided")}

Please create a compelling and well-structured presentation.""",
                    ),
                ]
            )

            response = self.llm.invoke(prompt.format_messages())

            # Parse the JSON response
            try:
                structure = json.loads(response.content)
            except json.JSONDecodeError:
                # If JSON parsing fails, try to extract JSON from the response
                content = response.content
                start_idx = content.find("{")
                end_idx = content.rfind("}") + 1
                if start_idx != -1 and end_idx != 0:
                    structure = json.loads(content[start_idx:end_idx])
                else:
                    raise ValueError("Unable to parse JSON from response")

            state["presentation_structure"] = structure

            return state
        except Exception as e:
            state["error"] = f"Error creating structure: {str(e)}"
            return state

    def _generate_slides(self, state: PresentationState) -> PresentationState:
        """Generate HTML/CSS/JS for the slides"""
        try:
            structure = state["presentation_structure"]

            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are an expert web developer and designer. Create beautiful, modern HTML slides with CSS and JavaScript.

Create a complete HTML document with:
1. Modern, professional styling with CSS
2. Responsive design
3. Smooth transitions between slides
4. Navigation controls
5. Beautiful typography and layout
6. Consistent theme throughout

Use modern web technologies and make it visually appealing. Include inline CSS and JavaScript in the HTML file.
Make sure the HTML is valid and complete - start with <!DOCTYPE html> and include all necessary tags.""",
                    ),
                    (
                        "human",
                        f"""Create HTML slides for this presentation structure:

{json.dumps(structure, indent=2)}

User Prompt Context: {state["user_prompt"]}

Make the slides visually stunning, professional, and easy to navigate. Include all the content from the structure.""",
                    ),
                ]
            )

            response = self.llm.invoke(prompt.format_messages())
            state["slides_html"] = response.content

            return state
        except Exception as e:
            state["error"] = f"Error generating slides: {str(e)}"
            return state

    def _generate_notes(self, state: PresentationState) -> PresentationState:
        """Generate detailed speaker notes"""
        try:
            structure = state["presentation_structure"]

            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are an expert public speaking coach. Create detailed speaker notes for each slide that help the presenter deliver an engaging and informative presentation.

For each slide, provide:
1. Opening statements and transitions
2. Key talking points with examples
3. Potential questions to engage the audience
4. Timing suggestions
5. Tips for delivery

Make the notes comprehensive but easy to follow during the presentation.""",
                    ),
                    (
                        "human",
                        f"""Create detailed speaker notes for this presentation:

{json.dumps(structure, indent=2)}

User Context: {state["user_prompt"]}
Document Content: {state.get("document_content", "No supporting documents")}

Provide comprehensive speaker notes that will help deliver an excellent presentation.""",
                    ),
                ]
            )

            response = self.llm.invoke(prompt.format_messages())
            state["speaker_notes"] = response.content

            return state
        except Exception as e:
            state["error"] = f"Error generating speaker notes: {str(e)}"
            return state

    def _generate_script(self, state: PresentationState) -> PresentationState:
        """Generate a complete presentation script"""
        try:
            structure = state["presentation_structure"]

            prompt = ChatPromptTemplate.from_messages(
                [
                    (
                        "system",
                        """You are an expert speechwriter. Create a complete, word-for-word presentation script that flows naturally and engages the audience.

The script should:
1. Have smooth transitions between slides
2. Be conversational and engaging
3. Include natural pauses and emphasis
4. Incorporate storytelling elements
5. Have a strong opening and closing
6. Be timed appropriately for each slide

Write it as if someone is speaking naturally to an audience.""",
                    ),
                    (
                        "human",
                        f"""Create a complete presentation script for:

{json.dumps(structure, indent=2)}

User Context: {state["user_prompt"]}
Document Content: {state.get("document_content", "No supporting documents")}

Write a compelling, natural-sounding script that brings the presentation to life.""",
                    ),
                ]
            )

            response = self.llm.invoke(prompt.format_messages())
            state["script"] = response.content

            return state
        except Exception as e:
            state["error"] = f"Error generating script: {str(e)}"
            return state

    def generate_presentation(
        self, user_prompt: str, documents: Optional[List[Dict]] = None
    ) -> Dict:
        """Main method to generate a complete presentation"""
        initial_state = PresentationState(
            user_prompt=user_prompt,
            documents=documents or [],
            document_content="",
            presentation_structure={},
            slides_html="",
            speaker_notes="",
            script="",
            error="",
        )

        try:
            result = self.workflow.invoke(initial_state)

            if result.get("error"):
                return {"error": result["error"]}

            return {
                "presentation_structure": result["presentation_structure"],
                "slides_html": result["slides_html"],
                "speaker_notes": result["speaker_notes"],
                "script": result["script"],
                "generated_at": datetime.now().isoformat(),
            }
        except Exception as e:
            return {"error": f"Workflow execution failed: {str(e)}"}


# Example usage
if __name__ == "__main__":
    agent = PresentationAgent()

    # Example generation
    result = agent.generate_presentation(
        user_prompt="Create a presentation about the benefits of renewable energy for a corporate audience",
        documents=[],
    )

    print("Presentation generated successfully!")
    print(f"Structure: {result.get('presentation_structure', {}).get('title', 'N/A')}")
