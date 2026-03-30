# 🛡️ VERIFY.AI Sentinel
### *Agentic Hallucination Auditor & Fact-Refinement Engine*

**VERIFY.AI Sentinel** is a high-precision auditing suite designed to combat LLM hallucinations. Built for the **Protex Hackathon**, it leverages a **Multi-Agent Swarm** to deconstruct claims, verify them against live web data, and provide an explainable "Trust Score" alongside a factually corrected version of the input.

---

## 🚀 Technical Highlights
* **Agentic Orchestration**: Powered by **CrewAI**, utilizing a sequential pipeline to transition from raw text to a verified audit.
* **Dual-Model Intelligence**: 
    * **Llama-3.1-8b-instant**: Optimized for high-speed factual extraction.
    * **Llama-3.3-70b-versatile**: Handles complex reasoning and final content refinement.
* **Real-Time Grounding**: Integration with **Serper Dev Tool** ensures audits are based on live, global data.
* **Deterministic Reliability**: Implementation of temperature=0 and **SHA256 hashing** ensures consistent, repeatable results for every audit.

---

## 🤖 The Sentinel Swarm (XAI in Action)
Sentinel provides **Explainable AI (XAI)** by breaking the "black box" of hallucination detection into four transparent stages:

1.  **Fact Extractor**: Identifies verifiable assertions within the text.
2.  **Grounding Specialist**: Acts as an investigative journalist, fetching live evidence for each claim.
3.  **Hallucination Auditor**: Analyzes contradictions to assign a **Trust Score (0-100%)**.
4.  **Content Refiner**: An editor-in-chief that rewrites the text to be 100% factual while maintaining tone.

---

## 🛠️ Installation & Setup

1.  **Clone the Repository**
2.  **Configure Environment**:
    * [cite_start]Create a `.env` file based on `.env.example`[cite: 2].
    * [cite_start]Add your `GROQ_API_KEY` and `SERPER_API_KEY`[cite: 1, 2].
3.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
4.  **Launch the Sentinel**:
    ```bash
    streamlit run app.py
    ```

---

## 🔑 Judge's Access (Prelims)
To access the **Sentinel Suite** dashboard:
* **IDENTIFIER**: `admin`
* **KEY**: `noida2026`

---

## 📊 System Overview
* **Backend**: Python, SQLite (Caching), CrewAI (Agentic Framework).
* **Frontend**: Streamlit with custom glassmorphism CSS.
* **Data Consistency**: Uses a deterministic SHA256 cache to prevent redundant API calls.

---
