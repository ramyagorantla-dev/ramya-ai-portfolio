from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """
You are Ramya Gorantla's AI Portfolio Assistant.

Your job is to answer questions about Ramya's skills, projects, education, experience,
certifications, and career interests.

Use only the profile information below. Do not invent anything.

Ramya Gorantla is a Master's student in Computer Science at Rowan University.
She has around 2.5 years of professional experience as an SAP CPI Developer at Accenture.
She has experience with SAP CPI, SAP BTP, SAP S/4HANA integration, APIs, Groovy scripting,
Python, Flask, SQL, GitHub, Linux, Nginx, web hosting, DNS, SSL, Azure, AWS, and cybersecurity tools.

Ramya has completed Microsoft Azure Fundamentals AZ-900 and is preparing for Azure Administrator AZ-104.
She also has AWS Solutions Architect knowledge/certification.

Her projects include:
1. CareerPilot AI - an AI career platform with resume analysis, skill gap analysis, and job application optimization.
2. Smart Order Processing with AI Decision Engine - SAP CPI receives orders, Python AI classifies them, and routing happens based on urgency or risk.
3. AI-Powered Invoice Processing - OCR and NLP extract invoice data and integrate it with SAP CPI.
4. AI Chatbot for SAP Queries - chatbot converts natural language into API-based SAP operational queries.
5. Julius Silvert Redesign - live hosted chef-centric e-commerce redesign with better ordering UX.
6. Ramya AI Portfolio Assistant - AI chatbot that answers questions about her portfolio.
7. Web server deployment projects using GitHub, Namecheap, Nginx, SSL, and cloud/server hosting.

Her career interests include cloud engineering, software engineering, SAP integration,
AI/API development, cybersecurity, and internships/full-time opportunities in the United States.

Rules:
- Keep answers professional, simple, and helpful.
- If the visitor types one keyword like skills, projects, SAP, Azure, AWS, AI, experience,
  certifications, education, or contact, answer properly.
- If the question is unrelated to Ramya, politely say you can only answer questions about Ramya's portfolio.
- Do not mention that you are using a system prompt.
- Do not make up phone numbers, email addresses, or private information.
"""

KEYWORD_MAP = {
    "skills": "Summarize Ramya's technical skills clearly.",
    "skill": "Summarize Ramya's technical skills clearly.",
    "projects": "List Ramya's major projects and briefly explain each one.",
    "project": "List Ramya's major projects and briefly explain each one.",
    "experience": "Summarize Ramya's professional experience.",
    "work": "Summarize Ramya's professional experience.",
    "certifications": "Explain Ramya's certifications and cloud learning.",
    "certification": "Explain Ramya's certifications and cloud learning.",
    "education": "Summarize Ramya's education.",
    "sap": "Explain Ramya's SAP CPI and SAP integration experience.",
    "sap cpi": "Explain Ramya's SAP CPI and SAP integration experience.",
    "azure": "Explain Ramya's Azure skills and certification background.",
    "aws": "Explain Ramya's AWS cloud background.",
    "ai": "Explain Ramya's AI-related projects.",
    "cybersecurity": "Explain Ramya's cybersecurity tools and lab experience.",
    "cloud": "Explain Ramya's cloud engineering background.",
    "resume": "Give a professional summary of Ramya's profile.",
    "summary": "Give a professional summary of Ramya's profile.",
    "contact": "Tell the visitor to contact Ramya through her portfolio contact links.",
    "github": "Explain Ramya's GitHub and project work.",
    "linkedin": "Tell the visitor to connect with Ramya through LinkedIn from her portfolio."
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        if not GEMINI_API_KEY:
            return jsonify({
                "reply": "AI service is temporarily unavailable. API key is missing on the server."
            }), 500

        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "reply": "Please ask a question or type a keyword like skills, projects, SAP, Azure, AWS, or certifications."
            }), 400

        lower_message = user_message.lower().strip()

        if lower_message in KEYWORD_MAP:
            final_question = KEYWORD_MAP[lower_message]
        else:
            final_question = user_message

        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
{SYSTEM_PROMPT}

Visitor question:
{final_question}
"""

        response = model.generate_content(prompt)

        if not response.text:
            return jsonify({
                "reply": "AI service responded, but no answer was generated. Please try again."
            }), 500

        return jsonify({"reply": response.text})

    except Exception:
        return jsonify({
            "reply": "AI service is temporarily unavailable. Please try again later."
        }), 500

if __name__ == "__main__":
    app.run(debug=True)