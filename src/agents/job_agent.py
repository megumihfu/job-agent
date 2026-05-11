from crewai import LLM
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
            CONTEXT: The candidate is looking for Backend/Cloud roles in France OR Germany.
            BENEFIT OF THE DOUBT: If the job description is missing or empty, but the JOB TITLE matches (DevOps, SRE, Cloud, Backend, Software Engineer) keep it.
            
            FILTERS:
            1. STACK: 
                - for backend/fullstack/software roles: must include either Python, Java, or Kotlin. 
                - for DevOps/SRE/Cloud: DO NOT reject if a langage isnt mentioned. 
            2. TECH FOCUS: REJECT non-IT jobs.
            3. EXPERIENCE: Entry-level to max 4 years.
            4. SECTOR: Only reject if the COMPANY itself is a Bank, Insurance, or Defense firm.
            5. CONTRACT: permanent or temporary. REJECT intern/apprentice & contract.
            6. LOCATION: The candidate accepts ALL cities in {job.get('target_country')}. 
            7. FINAL DECISION: If you are unsure or data is missing, the default answer is YES.

            DATA:
            - Job: {job.get('position')} @ {job.get('company')}
            - City: {job.get('location')}
            - Country Context: {job.get('target_country')}
            - Description: {job.get('description', 'N/A')[:600]}

            OUTPUT:
            YES or NO - [Explain why 'NO' with key words]
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