from src.agents.job_agent import run_job_agent

if __name__ == "__main__":
    try:
        run_job_agent()
    except Exception as e:
        print(f"Error IA agent: {e}")