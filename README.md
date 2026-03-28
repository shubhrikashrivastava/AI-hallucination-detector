# VERIFY.AI | Autonomous Hallucination Detector

VERIFY.AI is an agentic AI system designed to eliminate hallucinations in LLM outputs. It uses a **Multi-Agent Swarm** to extract claims, verify them via live web search (Active RAG), and audit the logical consistency of the output.

## 🚀 Features
- **Multi-Model Voting:** Splits tasks between Llama 3.3 70B and 8B to reduce bias.
- **Active RAG:** Real-time web grounding via Serper API.
- **Observability:** Professional dashboard with Trust Index metrics.

## 🛠️ Setup Instructions
1. Clone the repository.
2. Create a virtual environment: `python -m venv venv`.
3. Activate it: `.\venv\Scripts\Activate.ps1` (Windows).
4. Install dependencies: `pip install -r requirements.txt`.
5. Create a `.env` file based on `.env.example`.
6. Run: `streamlit run app.py`.

## 🤖 Architecture
- **Claim Extractor:** Atomic fact isolation.
- **Grounding Specialist:** Live web verification.
- **Hallucination Auditor:** Confidence scoring.
- **Content Refiner:** Fact-based reconstruction.
