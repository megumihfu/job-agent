import pytest
from unittest.mock import patch
from src.tools.linkedin_tool import LinkedInTool

@patch('src.tools.linkedin_tool.query')
def test_linkedin_tool_deduplication(mock_query):
    fake_job = {
        'jobUrl': 'https://linkedin.com/jobs/123',
        'position': 'DevOps Engineer',
        'company': 'FunnyName Company',
    }
    
    mock_query.return_value = [fake_job, fake_job]
    
    tool = LinkedInTool()
    
    results = tool._run()
    
    # check that only one job is kept after deduplication
    assert len(results) == 1  
    assert results[0]['jobUrl'] == 'https://linkedin.com/jobs/123'