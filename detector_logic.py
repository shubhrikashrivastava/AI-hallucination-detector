import os
import re
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

# Load Environment Variables
load_dotenv()

# --- 1. LLM CONFIGURATIONS ---
# Check for API Keys before starting
if not os.getenv("GROQ_API_KEY") or not os.getenv("SERPER_API_KEY"):
    raise ValueError("Missing API Keys! Please ensure your .env file is configured correctly.")

# Llama-3.1-8b for speed and high-limit extraction
fast_llm = LLM(model="groq/llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))

# Llama-3.3-70b for high-reasoning auditing and tool stability
heavy_llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))

search_tool = SerperDevTool()

# --- 2. AGENT DEFINITIONS ---
extractor = Agent(
    role='Factual Claim Extractor',
    goal='Identify every verifiable factual claim in: {input_text}',
    backstory='You are a forensic linguist. You strip away opinions to find core checkable facts.',
    llm=fast_llm,
    verbose=True
)

researcher = Agent(
    role='Grounding Specialist',
    goal='Verify claims using live web data. Always use the search tool.',
    backstory='You are an investigative researcher. You cross-reference claims with authoritative sources.',
    tools=[search_tool],
    llm=heavy_llm, 
    verbose=True,
    max_iter=3
)

auditor = Agent(
    role='Hallucination Auditor',
    goal='Compare original claims vs research findings. Calculate a Confidence Score (0-100).',
    backstory='You are a logic professor. You identify contradictions and assign a trust percentage.',
    llm=heavy_llm,
    verbose=True
)

corrector = Agent(
    role='Content Refiner',
    goal='Rewrite the original text to be 100% faithful to the discovered facts.',
    backstory='You are a senior editor. You fix hallucinations while maintaining the original tone.',
    llm=heavy_llm,
    verbose=True
)

# --- 3. EXECUTION WRAPPER ---
def run_hallucination_check(input_text):
    t1 = Task(description=f'Extract claims from: "{input_text}"', agent=extractor, expected_output='List of claims.')
    t2 = Task(description='Verify claims via web search.', agent=researcher, expected_output='Report with URLs.', context=[t1])
    t3 = Task(description='Audit claims vs evidence. Return a Score: X/100.', agent=auditor, expected_output='Audit report with score.', context=[t2])
    t4 = Task(description='Rewrite the original text based on audit.', agent=corrector, expected_output='The final corrected text.', context=[t3])

    crew = Crew(
        agents=[extractor, researcher, auditor, corrector],
        tasks=[t1, t2, t3, t4],
        process=Process.sequential,
        max_rpm=10, 
        verbose=True
    )

    return crew.kickoff(inputs={'input_text': input_text})