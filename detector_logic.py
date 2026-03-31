import os
import re
from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
from dotenv import load_dotenv

load_dotenv()

# Temperature=0 ensures deterministic, repeatable results for judges
fast_llm = LLM(model="groq/llama-3.1-8b-instant", temperature=0)
heavy_llm = LLM(model="groq/llama-3.3-70b-versatile", temperature=0)
search_tool = SerperDevTool()

def run_sentinel_audit(input_text):
    extractor = Agent(
        role='Fact Extractor',
        goal='Identify verifiable factual assertions.',
        backstory='Expert forensic linguist specializing in factual identification.',
        llm=fast_llm, max_rpm=15
    )

    researcher = Agent(
        role='Grounding Specialist',
        goal='Verify claims via live web data.',
        backstory='Investigative journalist checking real-time search results.',
        tools=[search_tool], llm=heavy_llm, max_iter=2, max_rpm=10
    )

    auditor = Agent(
        role='Hallucination Auditor',
        goal='Analyze contradictions and assign a Trust Score: X/100.',
        backstory='Data integrity expert focusing on model output reliability.',
        llm=heavy_llm, max_rpm=10
    )

    refiner = Agent(
        role='Content Refiner',
        goal='Rewrite the text to be 100% factual.',
        backstory='Editor-in-chief who preserves tone while fixing hallucinations.',
        llm=heavy_llm
    )

    t1 = Task(description=f"Extract facts from: {input_text}", agent=extractor, expected_output="Bulleted facts.")
    t2 = Task(description="Search for evidence.", agent=researcher, expected_output="URLs and findings.", context=[t1])
    t3 = Task(description="Calculate Trust Score: X/100.", agent=auditor, expected_output="Report with Score: X/100.", context=[t2])
    t4 = Task(description="Correct the original text.", agent=refiner, expected_output="Corrected version.", context=[t3])

    crew = Crew(
        agents=[extractor, researcher, auditor, refiner],
        tasks=[t1, t2, t3, t4],
        process=Process.sequential,
        verbose=True,
        cache=True # Native CrewAI caching for extra token savings
    )
    return crew.kickoff()
