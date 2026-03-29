import os
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

# LLM Setup
fast_llm = LLM(model="groq/llama-3.1-8b-instant", api_key=os.getenv("GROQ_API_KEY"))
heavy_llm = LLM(model="groq/llama-3.3-70b-versatile", api_key=os.getenv("GROQ_API_KEY"))
search_tool = SerperDevTool()

def run_hallucination_check(input_text):
    # 1. Extractor
    extractor = Agent(
        role='Fact Extractor',
        goal='List every factual claim in bullet points.',
        backstory='You are a meticulous researcher who ignores fluff and targets only facts.',
        llm=fast_llm
    )

    # 2. Researcher
    researcher = Agent(
        role='Internet Researcher',
        goal='Search for evidence supporting or debunking claims.',
        backstory='You have access to the real-time web. You provide URLs for every finding.',
        tools=[search_tool],
        llm=heavy_llm
    )

    # 3. Auditor (The Logic Engine)
    auditor = Agent(
        role='Fact Auditor',
        goal='Assign a score and identify lies.',
        backstory='You compare the researchers notes to the original text. You MUST include a final "Score: X/100" in your output.',
        llm=heavy_llm
    )

    # 4. Editor
    editor = Agent(
        role='Final Editor',
        goal='Rewrite the input text to be factual.',
        backstory='You take the audit findings and fix the original text without losing its style.',
        llm=heavy_llm
    )

    # Task Chain
    t1 = Task(description=f'Extract facts from: {input_text}', agent=extractor, expected_output='Bullet list of claims.')
    t2 = Task(description='Verify these claims using Google Search.', agent=researcher, expected_output='Verified findings with URLs.', context=[t1])
    t3 = Task(description='Audit the findings. Provide a Score: X/100 and list discrepancies.', agent=auditor, expected_output='Audit report with a Score.', context=[t2])
    t4 = Task(description='Rewrite the original text to be 100% accurate.', agent=editor, expected_output='The corrected text version.', context=[t3])

    crew = Crew(
        agents=[extractor, researcher, auditor, editor],
        tasks=[t1, t2, t3, t4],
        process=Process.sequential,
        verbose=True
    )

    return crew.kickoff()
