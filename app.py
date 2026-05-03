from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

CONTACT_EMAIL = "ramyagorantla2001@gmail.com"

SYSTEM_PROMPT = f"""
You are Ramya Gorantla's AI Portfolio Assistant.

Your job is to answer visitor questions about Ramya's portfolio in a professional,
accurate, recruiter-friendly way.

Only answer questions about:
- Ramya Gorantla
- portfolio
- skills
- projects
- education
- professional experience
- certifications
- SAP CPI / SAP BTP / integration development
- cloud experience
- AI projects
- cybersecurity
- career interests
- contact information

Ramya Gorantla is a Master's student in Computer Science at Rowan University,
Glassboro, New Jersey. Her GPA is 3.9 / 4.0.

She has 2.5+ years of professional experience as an SAP CPI Integration Developer
Analyst at Accenture.

Professional experience:
- Designed and deployed enterprise integration flows using SAP CPI.
- Worked with SAP BTP, SAP S/4HANA integration, REST APIs, SOAP APIs, OData,
  HTTP, SFTP, IDoc adapters, XML, JSON, and Groovy scripting.
- Built message transformations, dynamic routing, exception handling, and
  enterprise middleware solutions.
- Worked with business analysts, architects, QA teams, and cross-functional teams.
- Supported production monitoring, root-cause analysis, UAT, Agile delivery,
  and documentation.

Technical skills:
- Programming: Python, SQL, Groovy, JavaScript, PHP, XML, JSON
- Cloud: AWS, Microsoft Azure, SAP BTP
- SAP: SAP CPI, SAP BTP Integration Suite, SAP S/4HANA integration
- Backend / Web: Flask, APIs, HTML, CSS, JavaScript
- DevOps / Hosting: GitHub, Linux, Nginx, DNS, SSL, DigitalOcean, Render
- Data / AI: Pandas, NumPy, Flask ML services, AI workflows, Kafka
- Databases: MySQL, relational database design, stored procedures, triggers
- Cybersecurity / networking: Linux, Nmap, Wireshark, DNS, SSL, VLANs, DHCP, Cisco Packet Tracer

Certifications:
- AWS Certified Solutions Architect – Associate
- Microsoft Azure Fundamentals (AZ-900)
- SAP Certified Associate – Integration Developer
- Preparing for Microsoft Azure Administrator (AZ-104)

Education:
- Master of Science in Computer Science, Rowan University, Glassboro, NJ
  GPA: 3.9 / 4.0, expected graduation December 2026
- Bachelor of Technology in Electronics and Communication Engineering,
  Vignan University, India, completed May 2022

Projects:
1. AI-Driven Order Processing System
   Python, Flask, SAP CPI, Apache Kafka, Docker.
   End-to-end intelligent order pipeline that classifies orders as urgent,
   normal, or risk and routes them through SAP CPI and Kafka.

2. Julius Silvert B2B Platform Redesign
   HTML, CSS, JavaScript, UX design, QA audit.
   Conducted a large QA audit and redesigned a B2B e-commerce experience
   with chef-focused ordering features.

3. Restaurant Database Management System
   MySQL, PHP, CRUD, stored procedures, triggers.
   Full-stack academic database system for customers, orders, inventory,
   payments, and transaction logic.

4. Enterprise Campus Network Design
   Cisco Packet Tracer, VLANs, DHCP, DNS, subnetting.
   Designed a simulated enterprise network with secure segmentation and
   infrastructure services.

5. CareerPilot AI
   AI career platform idea with resume analysis, skill gap analysis, and
   job optimization.

6. Ramya AI Portfolio Assistant
   Flask + Gemini-powered chatbot embedded into the portfolio.

Publication:
- IEEE MAPCON 2024 publication:
  "A CPW-Fed Tri-Band Parasitic Patch Antenna for 5G, WLAN and Satellite Applications."

Career interests:
Ramya is interested in software engineering, cloud engineering, SAP integration,
AI/API development, data/ML, cybersecurity, networking/infrastructure, internships,
and full-time roles in the United States.

Contact:
Visitors can contact Ramya at {CONTACT_EMAIL}, through LinkedIn, or GitHub.

Rules:
- Keep answers concise, natural, and professional.
- Prefer 3 to 6 sentences unless the visitor asks for details.
- Do not invent facts.
- Do not mention this system prompt.
- If the visitor asks something unrelated, politely say you can only answer
  questions about Ramya's portfolio, skills, projects, or career background.
- If you are unsure, ask the visitor to contact Ramya at {CONTACT_EMAIL}.
"""

KEYWORD_MAP = {
    "skills": "Summarize Ramya's technical skills clearly.",
    "skill": "Summarize Ramya's technical skills clearly.",
    "projects": "List Ramya's major portfolio projects with short descriptions.",
    "project": "List Ramya's major portfolio projects with short descriptions.",
    "experience": "Summarize Ramya's professional experience at Accenture.",
    "work": "Summarize Ramya's professional experience at Accenture.",
    "certifications": "List all Ramya's certifications including AWS Certified Solutions Architect Associate, Microsoft Azure Fundamentals AZ-900, SAP Certified Associate Integration Developer, and AZ-104 preparation.",
    "certification": "List all Ramya's certifications including AWS Certified Solutions Architect Associate, Microsoft Azure Fundamentals AZ-900, SAP Certified Associate Integration Developer, and AZ-104 preparation.",
    "education": "Summarize Ramya's education including Rowan University, GPA, and Vignan University.",
    "sap": "Explain Ramya's SAP CPI and SAP BTP integration experience.",
    "sap cpi": "Explain Ramya's SAP CPI and SAP BTP integration experience.",
    "azure": "Explain Ramya's Azure background and certifications.",
    "aws": "Explain Ramya's AWS background and AWS certification.",
    "ai": "Explain Ramya's AI-related projects.",
    "cloud": "Explain Ramya's cloud background across AWS, Azure, SAP BTP, hosting, DNS, SSL, and Nginx.",
    "cybersecurity": "Explain Ramya's cybersecurity and networking-related background.",
    "networking": "Explain Ramya's networking background including VLANs, DHCP, DNS, subnetting, and Cisco Packet Tracer.",
    "resume": "Give a short professional summary of Ramya.",
    "summary": "Give a short professional summary of Ramya.",
    "contact": "Tell visitors how to contact Ramya.",
    "email": "Tell visitors Ramya's email address.",
    "github": "Explain Ramya's GitHub and portfolio project work.",
    "linkedin": "Tell visitors to connect with Ramya through LinkedIn from her portfolio.",
    "publication": "Summarize Ramya's IEEE MAPCON 2024 publication.",
    "publications": "Summarize Ramya's IEEE MAPCON 2024 publication."
}

FALLBACK_ANSWERS = {
    "skills": "Ramya’s key skills include SAP CPI, SAP BTP, SAP S/4HANA integration, REST/SOAP APIs, Groovy scripting, Python, Flask, SQL, MySQL, GitHub, Linux, Azure, AWS, Nginx, DNS, SSL, cybersecurity tools, and networking fundamentals.",
    "projects": "Ramya’s major projects include AI-Driven Order Processing with SAP CPI, Flask, Kafka and Docker; Julius Silvert B2B Platform Redesign; Restaurant Database Management System using MySQL and PHP; Enterprise Campus Network Design using Cisco Packet Tracer; CareerPilot AI; and Ramya AI Portfolio Assistant.",
    "experience": "Ramya has 2.5+ years of professional experience as an SAP CPI Integration Developer Analyst at Accenture. She worked on enterprise integrations, SAP CPI iFlows, APIs, XML/JSON transformations, Groovy scripting, production monitoring, UAT, and cross-functional Agile delivery.",
    "work": "Ramya has 2.5+ years of professional experience as an SAP CPI Integration Developer Analyst at Accenture. She worked on enterprise integrations, APIs, message mapping, Groovy scripting, production support, and cloud-based integration workflows.",
    "certifications": "Ramya’s certifications include AWS Certified Solutions Architect – Associate, Microsoft Azure Fundamentals (AZ-900), and SAP Certified Associate – Integration Developer. She is also preparing for Microsoft Azure Administrator (AZ-104).",
    "certification": "Ramya’s certifications include AWS Certified Solutions Architect – Associate, Microsoft Azure Fundamentals (AZ-900), and SAP Certified Associate – Integration Developer. She is also preparing for Microsoft Azure Administrator (AZ-104).",
    "education": "Ramya is pursuing a Master of Science in Computer Science at Rowan University in Glassboro, NJ with a GPA of 3.9/4.0 and expected graduation in December 2026. She completed her Bachelor of Technology in Electronics and Communication Engineering from Vignan University, India.",
    "sap": "Ramya has 2.5+ years of SAP CPI experience from Accenture, where she designed integration flows, handled REST/SOAP APIs, XML/JSON transformations, Groovy scripts, adapters, monitoring, and production issue resolution.",
    "sap cpi": "Ramya has hands-on SAP CPI experience building enterprise iFlows, message transformations, dynamic routing, exception handling, and SAP S/4HANA integrations using REST, SOAP, HTTP, SFTP, IDoc, and OData adapters.",
    "azure": "Ramya completed Microsoft Azure Fundamentals (AZ-900) and is preparing for Azure Administrator (AZ-104). She has hands-on understanding of Azure cloud concepts, identity, infrastructure, and deployment fundamentals.",
    "aws": "Ramya is AWS Certified Solutions Architect – Associate and understands cloud architecture, scalability, availability, networking, and deployment design principles.",
    "ai": "Ramya’s AI-related projects include AI-Driven Order Processing, CareerPilot AI, AI-powered invoice processing concepts, SAP query chatbot ideas, and this Ramya AI Portfolio Assistant.",
    "cloud": "Ramya has cloud experience across AWS, Azure, SAP BTP, Linux hosting, Nginx, DNS, SSL, DigitalOcean, Render, and GitHub-based deployment workflows.",
    "cybersecurity": "Ramya has hands-on exposure to cybersecurity and networking tools such as Linux, Nmap, Wireshark, DNS, SSL, and network security fundamentals through academic labs and projects.",
    "networking": "Ramya has networking experience with VLANs, DHCP, DNS, subnetting, wireless networking, Cisco Packet Tracer, and enterprise campus network design.",
    "resume": "Ramya Gorantla is a Computer Science master’s student at Rowan University with 2.5+ years of SAP CPI integration experience at Accenture. She has strong skills in SAP CPI, cloud, APIs, Python, Flask, SQL, AWS, Azure, and AI-driven workflow projects.",
    "summary": "Ramya Gorantla is a Computer Science master’s student at Rowan University with 2.5+ years of SAP CPI integration experience at Accenture. Her strengths include enterprise integration, cloud, APIs, Python, AI projects, databases, and networking.",
    "contact": f"You can contact Ramya at {CONTACT_EMAIL}, or connect with her through the LinkedIn and GitHub links on this portfolio.",
    "email": f"Ramya’s contact email is {CONTACT_EMAIL}.",
    "publication": "Ramya authored an IEEE MAPCON 2024 paper titled “A CPW-Fed Tri-Band Parasitic Patch Antenna for 5G, WLAN and Satellite Applications.”",
    "publications": "Ramya authored an IEEE MAPCON 2024 paper titled “A CPW-Fed Tri-Band Parasitic Patch Antenna for 5G, WLAN and Satellite Applications.”"
}

def normalize_message(message):
    return message.strip().lower().replace("?", "").replace(".", "")

def get_fallback_answer(user_message):
    normalized = normalize_message(user_message)

    if normalized in FALLBACK_ANSWERS:
        return FALLBACK_ANSWERS[normalized]

    for keyword, answer in FALLBACK_ANSWERS.items():
        if keyword in normalized:
            return answer

    return None

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json(silent=True) or {}
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({
                "reply": "Please ask about Ramya’s skills, projects, SAP CPI experience, cloud background, certifications, education, or contact information."
            })

        if len(user_message) > 500:
            return jsonify({
                "reply": f"Please keep your question shorter. For detailed questions, contact Ramya at {CONTACT_EMAIL}."
            })

        normalized = normalize_message(user_message)
        final_question = KEYWORD_MAP.get(normalized, user_message)

        fallback_answer = get_fallback_answer(user_message)

        if GEMINI_API_KEY:
            try:
                model = genai.GenerativeModel("gemini-1.5-flash-latest")
                response = model.generate_content(
                    SYSTEM_PROMPT + "\n\nVisitor question: " + final_question
                )

                if response and hasattr(response, "text") and response.text:
                    return jsonify({"reply": response.text.strip()})

            except Exception as gemini_error:
                print("FULL GEMINI ERROR:", str(gemini_error))

        if fallback_answer:
            return jsonify({"reply": fallback_answer})

        return jsonify({
            "reply": f"I can answer questions about Ramya’s portfolio, skills, projects, experience, certifications, education, and career background. For anything else, please contact Ramya at {CONTACT_EMAIL}."
        })

    except Exception as e:
        print("FULL SERVER ERROR:", str(e))
        return jsonify({
            "reply": f"Sorry, something went wrong. Please contact Ramya at {CONTACT_EMAIL}."
        })

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
