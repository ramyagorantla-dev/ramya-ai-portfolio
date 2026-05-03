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

Answer questions only about Ramya Gorantla's portfolio, skills, projects, education,
experience, certifications, SAP CPI background, cloud experience, AI projects,
and career interests.

Ramya Gorantla is a Master's student in Computer Science at Rowan University.
She has 2.5+ years of professional experience as an SAP CPI Developer at Accenture.
Her skills include SAP CPI, SAP BTP, SAP S/4HANA integration, APIs, Groovy scripting,
Python, Flask, SQL, GitHub, Linux, Nginx, web hosting, DNS, SSL, Azure, AWS,
and cybersecurity tools.

She completed Microsoft Azure Fundamentals AZ-900 and is preparing for AZ-104.
She also has AWS Solutions Architect knowledge/certification.

Her projects include CareerPilot AI, Smart Order Processing with AI Decision Engine,
AI-Powered Invoice Processing, AI Chatbot for SAP Queries, Julius Silvert Redesign,
Web Server Deployment projects, and Ramya AI Portfolio Assistant.

Keep answers professional, short, and helpful.
If the visitor asks unrelated questions, say you can only answer about Ramya's portfolio.
Do not invent information.
"""

KEYWORD_MAP = {
    "skills": "Summarize Ramya's technical skills.",
    "skill": "Summarize Ramya's technical skills.",
    "projects": "List Ramya's major projects.",
    "project": "List Ramya's major projects.",
    "experience": "Summarize Ramya's professional experience.",
    "certifications": "Explain Ramya's certifications.",
    "certification": "Explain Ramya's certifications.",
    "education": "Summarize Ramya's education.",
    "sap": "Explain Ramya's SAP CPI experience.",
    "sap cpi": "Explain Ramya's SAP CPI experience.",
    "azure": "Explain Ramya's Azure background.",
    "aws": "Explain Ramya's AWS background.",
    "ai": "Explain Ramya's AI-related projects.",
    "cloud": "Explain Ramya's cloud background.",
    "cybersecurity": "Explain Ramya's cybersecurity background.",
    "contact": "Tell visitors to contact Ramya through her portfolio contact links."
}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip() if data else ""

        if not user_message:
            return jsonify({
                "reply": "Please ask a question or type skills, projects, SAP, Azure, AWS, or certifications."
            })

        if not GEMINI_API_KEY:
            return jsonify({
                "reply": "AI service is temporarily unavailable because the API key is missing."
            })

        lower_message = user_message.lower()
        final_question = KEYWORD_MAP.get(lower_message, user_message)

        model = genai.GenerativeModel("gemini-1.5-flash")

        response = model.generate_content(
            SYSTEM_PROMPT + "\n\nVisitor question: " + final_question
        )

        reply = response.text if response and response.text else "Sorry, I could not generate a response."

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({
            "reply": "AI service is temporarily unavailable. Please try again later."
        })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)