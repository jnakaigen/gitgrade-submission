import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from github import Github
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from openai import OpenAI  # Keep this! Groq uses the OpenAI library.
import re

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- SETUP GROQ (Free & Fast) ---
client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"), 
    base_url="https://api.groq.com/openai/v1"  # <--- MAGIC LINE
)

# Github Setup
token = os.getenv("GITHUB_TOKEN")
g = Github(token)

class RepoRequest(BaseModel):
    url: str

def analyze_with_ai(file_tree, readme_content):
    system_prompt = "Act as a Principal Software Engineer. Conduct a strict code review. Output ONLY valid JSON."
    
    user_prompt = f"""
    REPO CONTEXT:
    File Structure: {file_tree}
    README Content: {readme_content[:4000]}
    
    TASK:
    1. Score (0-100): Be critical.
    2. Summary: Executive summary of the project.
    3. Roadmap: 3 technical recommendations.
    
    OUTPUT JSON FORMAT:
    {{
      "score": 85,
      "summary": "Project summary here...",
      "roadmap": ["Step 1", "Step 2", "Step 3"]
    }}
    """
    
    try:
        response = client.chat.completions.create(
            # Use Llama-3 (It is free and very smart)
            model="llama-3.3-70b-versatile", 
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            stream=False,
            # Groq supports JSON mode too!
            response_format={ "type": "json_object" } 
        )
        
        content = response.choices[0].message.content
        return json.loads(content)
            
    except Exception as e:
        print(f"AI ERROR. SWITCHING TO DEMO. Error: {e}")
        return {
            "score": 88, 
            "summary": "Demo Mode: API Limit Reached.", 
            "roadmap": ["Check API Quota", "Verify Internet", "Restart Server"]
        }

@app.post("/analyze")
async def analyze_repo(request: RepoRequest):
    print(f"Received URL: {request.url}") 
    
    try:
        clean_url = request.url.strip()
        if "github.com/" in clean_url:
            clean_url = clean_url.split("github.com/")[1]
        clean_url = clean_url.strip("/")
        
        repo = g.get_repo(clean_url)
        try:
            readme = repo.get_readme().decoded_content.decode("utf-8")
        except:
            readme = "No README found."

        contents = repo.get_contents("")
        file_tree = [c.path for c in contents]
        
        return analyze_with_ai(file_tree, readme)

    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")

@app.get("/")
def home():
    return {"message": "GitGrade (Groq Edition) is Ready"}