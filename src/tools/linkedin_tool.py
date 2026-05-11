from linkedin_jobs_api import query
from crewai.tools import BaseTool
import time

class LinkedInTool(BaseTool):
    name: str = "Linkedin job search"
    description: str = "Search jobs on linkedin and return raw data"
    
    def _run(self) -> list:
        keywords = ["devops", "cloud engineer", "backend engineer"]
        job_types = ["full time", "temporary"]
        experience = ["entry level", "associate"]
        locations = ["France", "Germany"]

        all_jobs = []

        for loc in locations:
            print(f"\nSearching in {loc}...")
            
            for keyword in keywords:
                for job_type in job_types:
                    for xp in experience:

                        try:
                            jobs = query(
                                keyword=keyword,
                                location=loc,
                                date_since_posted="24hr",
                                experience_level=xp,
                                job_type=job_type,
                                limit=10
                            )

                            if jobs:
                                print(f"{len(jobs)} jobs found for {keyword} in {loc}")
                                for job in jobs:
                                    job['target_country'] = loc
                                all_jobs.extend(jobs)

                            else:
                                print(f"No job found for {keyword}")

                        except Exception as e:
                            print(f"Error: {e}")

                        time.sleep(1)

        unique_jobs = {}

        for job in all_jobs:
            url = job.get('jobUrl', '')
            if url and url not in unique_jobs:
                unique_jobs[url] = job
        
        final_jobs = list(unique_jobs.values())

        return final_jobs