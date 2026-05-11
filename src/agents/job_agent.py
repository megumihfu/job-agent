from crewai import Agent, Task, Crew, LLM
from langchain_openai import ChatOpenAI
from src.config import CHATANYWHERE_API_KEY
from src.tools.linkedin_tool import LinkedInTool
from src.tools.excel_tool import ExcelExportTool
import json

# LLM agent conf
llm = LLM(
    model="gpt-4o-mini",
    api_key=CHATANYWHERE_API_KEY,
    base_url="https://api.chatanywhere.tech/v1",
    temperature=0.1
)

print("LLM has been configured")

linkedin_tool = LinkedInTool()
excel_tool = ExcelExportTool()

def run_job_agent():
    print("Starting job agent...")
    
    job_offers = linkedin_tool._run()

    valid_jobs = []

    for job in job_offers:
        prompt = f"""
            ROLE: Expert IT Recruitment Screener.
            CONTEXT: The candidate is looking for Backend/DevOps roles in France OR Germany.
            
            FILTERS:
            1. DEVELOPER STACK: Must be related to Python, Java, or Kotlin. 
            2. TECH FOCUS: REJECT non-IT jobs.
            3. EXPERIENCE: Entry-level to max 4 years.
            4. SECTORS: REJECT Banking, Insurance, Defense.
            5. CONTRACT: permanent or temporary. REJECT intern/apprentice & contract.
            6. LOCATION: The candidate accepts ALL cities in {job.get('target_country')}. 
            7. UNKNOWN: If Salary/Exp is missing, assume YES.

            DATA:
            - Job: {job.get('position')} @ {job.get('company')}
            - City: {job.get('location')}
            - Country Context: {job.get('target_country')}
            - Description: {job.get('description', 'N/A')[:600]}

            OUTPUT:
            YES or NO - [Explain why 'NO' in a quick note]
        """

        response = llm.call(prompt)
        print(f"{job.get('position', '')[:40]}... {response.strip()}")

        if "YES" in response.upper():
            valid_jobs.append(job)

    if valid_jobs:
        print(f"{len(valid_jobs)} valid offers. Exporting to excel...")
        jobs_json = json.dumps(valid_jobs, default=str)
        result = excel_tool._run(jobs_json)
        print(result)
    else:
        print("No job offer found.")


if __name__ == "__main__":
    run_job_agent()