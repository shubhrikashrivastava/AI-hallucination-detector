import os
import re
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# 1. Load Environment Variables
load_dotenv()

# Check for API Keys before starting
if not os.getenv("GROQ_API_KEY") or not os.getenv("SERPER_API_KEY"):
    raise ValueError("Missing API Keys! Please ensure your .env file is configured correctly.")

# --- 2. LLM CONFIGURATIONS ---

# Llama-3.1-8b: High speed for simple parsing (Claim Extraction)
fast_llm = LLM(
    model="groq/llama-3.1-8b-instant", 
    api_key=os.getenv("GROQ_API_KEY")
)

# Llama-3.3-70b: High reasoning & stable tool-use (Research & Auditing)
heavy_llm = LLM(
    model="groq/llama-3.3-70b-versatile", 
    api_key=os.getenv("GROQ_API_KEY")
)

# Tool for live web search
search_tool = SerperDevTool()

# --- 3. AGENT DEFINITIONS ---

extractor = Agent(
    role='Factual Claim Extractor',
    goal='Identify every verifiable factual claim in: {input_text}',
    backstory='You are a forensic linguist. You strip away opinions to find core checkable facts.',
    llm=fast_llm,
    verbose=True,
    allow_delegation=False
)

researcher = Agent(
    role='Grounding Specialist',
    goal='Verify claims using live web data. Always use the search tool.',
    backstory='You are an investigative researcher. You cross-reference claims with authoritative sources.',
    tools=[search_tool],
    llm=heavy_llm,  # Switched to 70B for stable Tool-Calling
    verbose=True,
    max_iter=3,
    allow_delegation=False
)

auditor = Agent(
    role='Hallucination Auditor',
    goal='Compare original claims vs research findings. Calculate a Confidence Score (0-100).',
    backstory='You are a logic professor. You identify contradictions and assign a trust percentage.',
    llm=heavy_llm, # 70B for deep reasoning
    verbose=True,
    allow_delegation=False
)

corrector = Agent(
    role='Content Refiner',
    goal='Rewrite the original text to be 100% faithful to the discovered facts.',
    backstory='You are a senior editor. You fix hallucinations while maintaining the original tone.',
    llm=heavy_llm, # 70B for high-quality rewriting
    verbose=True,
    allow_delegation=False
)

# --- 4. EXECUTION WRAPPER ---

def run_hallucination_check(input_text):
    # Task 1: Find the facts
    t1 = Task(
        description=f'Extract all verifiable claims from this text: "{input_text}"', 
        agent=extractor, 
        expected_output='A bulleted list of verifiable factual assertions.'
    )
    
    # Task 2: Search the web
    t2 = Task(
        description='Take the claims and verify them using the search tool. Look for primary sources.', 
        agent=researcher, 
        expected_output='A summary of findings for each claim with supporting URLs.', 
        context=[t1]
    )
    
    # Task 3: Audit and Score
    t3 = Task(
        description='Compare the findings to the original claims. If a claim is false, flag it. Provide a final Score: X/100.', 
        agent=auditor, 
        expected_output='An audit report showing matches/conflicts and a final Score: X/100.', 
        context=[t2]
    )
    
    # Task 4: Fix the content
    t4 = Task(
        description='Rewrite the original input text to correct any inaccuracies found. Keep it professional.', 
        agent=corrector, 
        expected_output='The final corrected version of the text.', 
        context=[t3]
    )

    # Crew Orchestration
    crew = Crew(
        agents=[extractor, researcher, auditor, corrector],
        tasks=[t1, t2, t3, t4],
        process=Process.sequential,
        max_rpm=10, # Safety throttle for free tier
        verbose=True
    )

    return crew.kickoff(inputs={'input_text': input_text})
