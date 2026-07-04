# AI Smart Village Development Planner

AI-powered rural development planning system for Indian villages using **FastAPI**, **React**, and **LLM**.

Village development planning is often done manually and requires experts from multiple domains. This AI system analyzes village data and generates recommendations automatically — helping government officials, NGOs, and village administrators plan rural development efficiently.

## Features

- **Agriculture Advisor** — Crop recommendations based on rainfall, soil type, and area
- **Water Management** — Borewell, check dam, and rainwater harvesting plans
- **Healthcare Planner** — PHC requirements, mobile clinics, telemedicine suggestions
- **Education Planner** — School infrastructure, teacher requirements, digital classrooms
- **Government Schemes** — Maps 7+ central government schemes to village needs
- **Budget Optimizer** — Estimates total development cost across all modules
- **Interactive Map** — Shows village location using Leaflet + OpenStreetMap
- **PDF Report** — Generates downloadable development report

#Tech Stack
Backend: Python 3.11, FastAPI, SQLAlchemy, PostgreSQL, Uvicorn
Frontend: React.js, Axios, Leaflet, jsPDF, Recharts
AI: Rule-based intelligent modules + Ollama Llama3 (local LLM)

#Folder Structure
smart-village-planner/
├── backend/
│   ├── main.py
│   ├── database.py
│   ├── schemas.py
│   ├── modules/
│   │   ├── agriculture.py
│   │   ├── water.py
│   │   ├── healthcare.py
│   │   ├── education.py
│   │   ├── schemes.py
│   │   └── analyzer.py
│   └── routes/
│       ├── villages.py
│       └── ai_modules.py
└── frontend/
    └── src/
        ├── App.js
        └── App.css

# How to Run
Backend:
cd backend
python -m venv venv
venv\Scripts\activate
pip install fastapi uvicorn sqlalchemy psycopg2-binary pandas python-dotenv python-multipart httpx pydantic
python database.py
uvicorn main:app --reload --port 8000

Frontend:
cd frontend
npm install
npm start

# Government Schemes Covered
PM Krishi Sinchai Yojana — Free drip irrigation
Jal Jeevan Mission — Piped water to every household
Ayushman Bharat — Rs.5 lakh health insurance
National Health Mission — PHC construction
Samagra Shiksha Abhiyan — School construction
MNREGA — 100 days guaranteed employment
PM Awaas Yojana — Free house construction
Smart Village Initiative — WiFi and digital services

# Problem Statement
Village development planning is often done manually and requires experts from multiple domains. This AI system analyzes village data and generates recommendations automatically — helping government officials, NGOs, and village administrators plan rural development efficiently.

# Future Scope
Multilingual support (Kannada, Tamil, Telugu, Hindi)
Voice input and output
RAG-based government document retrieval
Mobile app version
Real-time satellite data integration
