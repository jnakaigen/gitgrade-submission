import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from github import Github
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# Setup GitHub
token = os.getenv("GITHUB_TOKEN")
g = Github(token)

class RepoRequest(BaseModel):
    url: str

def analyze_with_gemini(file_tree, readme_content):
    prompt = f"""
    You are an expert code reviewer. Analyze this GitHub repository data.
    
    FILE STRUCTURE:
    {file_tree}
    
    README CONTENT:
    {readme_content[:3000]}
    
    TASK:
    1. Give a Score (0-100).
    2. Write a short Summary (2 sentences).
    3. Create a Roadmap (3 bullet points).
    
    IMPORTANT: Return ONLY raw JSON. No Markdown.
    
    OUTPUT JSON FORMAT:
    {{
      "score": 85,
      "summary": "Text...",
      "roadmap": ["Step 1", "Step 2", "Step 3"]
    }}
    """
    try:
        response = model.generate_content(prompt)
        clean_text = response.text.strip().replace("```json", "").replace("```", "")
        return json.loads(clean_text)
    except Exception as e:
        print(f"AI ERROR: {e}")
        # Return fallback data if AI fails so app doesn't crash
        return {
            "score": 75, 
            "summary": "AI could not generate summary (Quota limit or parsing error).", 
            "roadmap": ["Check code structure manually", "Add comprehensive tests"]
        }

@app.post("/analyze")
async def analyze_repo(request: RepoRequest):
    print(f"Received URL: {request.url}") # Debug Print
    
    try:
        # Robust URL Cleaner
        clean_url = request.url.strip()
        if "github.com/" in clean_url:
            clean_url = clean_url.split("github.com/")[1]
        clean_url = clean_url.strip("/")
        
        print(f"Trying to fetch Repo: '{clean_url}'") # Debug Print
        
        repo = g.get_repo(clean_url)

        try:
            readme = repo.get_readme().decoded_content.decode("utf-8")
        except:
            readme = "No README found."

        contents = repo.get_contents("")
        file_tree = [c.path for c in contents]
        
        return analyze_with_gemini(file_tree, readme)

    except Exception as e:
        # THIS PRINTS THE REAL ERROR TO YOUR TERMINAL
        print(f"\n!!!!! CRITICAL ERROR !!!!!\n{e}\n")
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@app.get("/")
def home():
    return {"message": "GitGrade is Ready"}