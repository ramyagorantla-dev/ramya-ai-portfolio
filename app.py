from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

FALLBACK_ANSWERS = {
    "skills": "Ramya’s key skills include SAP CPI, SAP BTP, SAP S/4HANA integration, APIs, Groovy scripting, Python, Flask, SQL, GitHub, Linux, Azure, AWS, Nginx, DNS, SSL, and cybersecurity tools.",
    "projects": "Ramya’s major projects include CareerPilot AI, Smart Order Processing with AI Decision Engine, AI-Powered Invoice Processing, AI Chatbot for SAP Queries, Julius Silvert Redesign, Web Server Deployment, and Ramya AI Portfolio Assistant.",
    "sap": "Ramya has 2.5+ years of experience as an SAP CPI Developer at Accenture, working on integrations, APIs, message transformations, middleware, and enterprise integration solutions.",
    "azure": "Ramya completed Microsoft Azure Fundamentals AZ-900 and is preparing for AZ-104. She has cloud knowledge in identity, infrastructure, and deployment concepts.",
    "aws": "Ramya has AWS Solutions Architect knowledge and uses AWS/cloud concepts in architecture, deployment, and real-world project design.",
    "certifications": "Ramya completed Microsoft Azure Fundamentals AZ-900, is preparing for Azure Administrator AZ-104, and has AWS Solutions Architect knowledge.",
    "experience": "Ramya has 2.5+ years of professional experience in SAP CPI development, cloud tools, middleware, APIs, message transformation, and enterprise integration.",
    "education": "Ramya is a Master's student in Computer Science at Rowan University.",
    "cloud": "Ramya has experience with Azure, AWS, cloud deployment, DNS, SSL, GitHub Pages, Render, and web hosting concepts.",
    "ai": "Ramya’s AI projects include CareerPilot AI, AI-powered invoice processing, Smart Order Processing with AI Decision Engine, and this AI Portfolio Assistant."
}

SYSTEM_PROMPT = """
You are Ramya Gorantla's AI Portfolio Assistant.
Answer only about Ramya's skills, projects, experience, education, certifications, SAP CPI, cloud, AWS, Azure, AI projects, and career interests.
Keep answers short, professional, and helpful.
Do not invent information.
"""

PROFILE_CONTEXT = """
Ramya Gorantla is a Master's student in Computer Science at Rowan University.
She has 2.5+ years of professional experience as an SAP CPI Developer at Accenture.
Skills: SAP CPI, SAP BTP, SAP S/4HANA integration, APIs, Groovy scripting, Python, Flask, SQL, GitHub, Linux, Azure, AWS, Nginx, DNS, SSL, cybersecurity tools.
Projects: CareerPilot AI, Smart Order Processing with AI Decision Engine, AI-Powered Invoice Processing, AI Chatbot for SAP Queries, Julius Silvert Redesign, Web Server Deployment, Ramya AI Portfolio Assistant.
"""

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message", "").strip() if data else ""

    if not user_message:
        return jsonify({"reply": "Please type skills, projects, SAP, Azure, AWS, certifications, experience, or education."})

    lower_message = user_message.lower()

    try:
        if GEMINI_API_KEY:
            model = genai.GenerativeModel("gemini-1.5-flash-latest")
            prompt = SYSTEM_PROMPT + "\n\n" + PROFILE_CONTEXT + "\n\nVisitor question: " + user_message
            response = model.generate_content(prompt)

            if response and response.text:
                return jsonify({"reply": response.text})

    except Exception as e:
        print("GEMINI ERROR:", str(e))

    for keyword, answer in FALLBACK_ANSWERS.items():
        if keyword in lower_message:
            return jsonify({"reply": answer})

    return jsonify({
        "reply": "Ramya has experience in SAP CPI, cloud technologies, Python, Flask, Azure, AWS, APIs, and AI-related projects. You can ask about skills, projects, SAP, Azure, AWS, certifications, education, or experience."
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
