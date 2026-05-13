import pytest
import json
import os
from unittest.mock import patch
from src.agents.job_agent import run_job_agent
from src.tools.excel_tool import ExcelExportTool


@patch('src.agents.job_agent.linkedin_tool._run')
@patch('src.agents.job_agent.llm.call')
@patch('src.agents.job_agent.excel_tool._run')
def test_job_agent_logic_yes(mock_excel, mock_llm, mock_linkedin):
    """Test if a job is validated when LLM returns "YES" & correctly exported to Excel"""
    mock_linkedin.return_value = [{
        'position': 'Backend Java developer',
        'company': 'FunnyName Company',
        'target_country': 'France'
    }]
    
    mock_llm.return_value = "YES"
    
    run_job_agent()
    
    args, _ = mock_excel.call_args
    import json
    exported_jobs = json.loads(args[0])
    assert len(exported_jobs) == 1
    assert exported_jobs[0]['position'] == 'Backend Java developer'

@patch('src.agents.job_agent.linkedin_tool._run')
@patch('src.agents.job_agent.llm.call')
@patch('src.agents.job_agent.excel_tool._run')
def test_job_agent_rejection(mock_excel, mock_llm, mock_linkedin):
    # Check if a "NO" job is not added to the exported list
    mock_linkedin.return_value = [{
        'position': 'DevOps',
        'company': 'BNP Paribas',
        'target_country': 'France'
    }]
    
    mock_llm.return_value = "NO - sector not allowed (banking)"
    
    from src.agents.job_agent import run_job_agent
    run_job_agent()
    
    args, _ = mock_excel.call_args
    assert args[0] == "[]"

@patch('src.agents.job_agent.linkedin_tool._run')
@patch('src.agents.job_agent.llm.call')
@patch('src.agents.job_agent.excel_tool._run')
def test_job_agent_quota_error(mock_excel, mock_llm, mock_linkedin):
    # Check if the agent handles LLM quota errors gracefully and still calls Excel export
    mock_linkedin.return_value = [{'position': 'DevOps', 'target_country': 'Germany'}]
    
    mock_llm.side_effect = Exception("Rate limit reached (429)")
    
    run_job_agent()
    
    mock_excel.assert_called_once()

def test_excel_tool_missing_fields():
    # check excel file exported even if fields are missing in job data
    tool = ExcelExportTool()
    
    incomplete_job = [{
        "position": "DevOps Engineer",
        "jobUrl": "https://somerandomcoolurl.com"
    }]
    
    result = tool._run(json.dumps(incomplete_job))
    
    assert "Excel file generated" in result
    assert len(os.listdir("outputs")) > 0