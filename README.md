# GitGrade 🚀 | AI-Powered GitHub Repository Evaluator

## GitGrade Demo

![gitgrade1](https://github.com/user-attachments/assets/dc1da22a-8103-456d-8ee0-7cc7ffba3e65)
![gitgrade2](https://github.com/user-attachments/assets/ada1e3bb-7d65-4d1f-a5f4-101df29d760a)
![gitgrade3](https://github.com/user-attachments/assets/6ef8e4f4-c22d-4f14-ab8c-cd161c362236)

## 💡 Overview
**GitGrade** is an intelligent developer tool built for the **[Hackathon Name]** that instantly audits GitHub repositories. By leveraging **Google Gemini Pro**, it analyzes file structures and documentation to provide a comprehensive quality score, executive summary, and actionable roadmap for improvement.

## 🎥 Demo Video
[🔴 WATCH THE DEMO VIDEO HERE]
https://drive.google.com/file/d/1WhqVruU8w9cU1FvFNTvZIhJE7o6t4e4b/view?usp=drive_link


## ✨ Key Features
* **AI-Powered Analysis:** Uses Google Gemini Pro to understand code context.
* **Instant Scoring:** Generates a quality score (0-100) based on best practices.
* **Actionable Roadmap:** Provides specific, technical steps to improve the codebase.
* **Modern UI:** Built with React & Glassmorphism design for a premium experience.

## 🛠️ Tech Stack
* **Frontend:** React + Vite (Glassmorphism UI)
* **Backend:** Python + FastAPI
* **AI Engine:** Google Gemini Pro (via `google-generativeai`)
* **Integration:** GitHub API (`PyGithub`)

---

## 🚀 How to Run Locally

### Prerequisites
* Node.js & npm installed
* Python 3.8+ installed
* A Google Gemini API Key
* A GitHub Personal Access Token

### 1. Clone the Repository
```bash
git clone [https://github.com/yourusername/gitgrade.git](https://github.com/yourusername/gitgrade.git)
cd gitgrade
2. Setup Backend (Python)
Bash

cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install -r requirements.txt
Create a .env file in the backend/ folder:

Code snippet

GITHUB_TOKEN=your_github_token_here
GEMINI_API_KEY=your_gemini_api_key_here
Start the Server:

Bash

uvicorn main:app --reload
3. Setup Frontend (React)
Open a new terminal:

Bash

cd frontend
npm install
npm run dev
Access the app at http://localhost:5173.

📌 Usage
Enter a valid GitHub Repository URL (e.g., https://github.com/fastapi/fastapi).

Click "Grade It".

Wait for the AI to analyze the file structure and README.

View your Score, Summary, and Personalized Roadmap.

```
🛡️ License
This project is open-source and available under the MIT License.
