import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from agents.instructor_nice import NiceInstructor
from agents.instructor_mean import MeanInstructor

# Create both instructors
nice_instructor = NiceInstructor(model="gpt-4o-mini")
mean_instructor = MeanInstructor(model="gpt-4o-mini")

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskRequest(BaseModel):
    question: str
    mode: str

@app.post("/api/ask")
async def ask(request: AskRequest):
    question = request.question.strip()
    mode = request.mode.strip().lower()
    
    if not question:
        return {"answer": "Please enter a question."}
    
    # Choose instructor based on mode
    if mode == "mean":
        instructor = mean_instructor
    else:
        instructor = nice_instructor
    
    try:
        result = await instructor.arun(question)
        return {"answer": result}
    except Exception as e:
        print(f"Error in agent execution: {e}")
        import traceback
        traceback.print_exc()
        return {"answer": f"Sorry, I encountered an error: {str(e)}"}

# Serve the frontend
@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")

app.mount("/static", StaticFiles(directory="static"), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)