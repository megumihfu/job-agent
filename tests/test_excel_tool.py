import pytest
import json
import os
import pandas as pd
from src.tools.excel_tool import ExcelExportTool

def test_excel_export_creates_file_and_checks_columns():
    # check if the tool creat an excel file with correct content"""
    tool = ExcelExportTool()
    
    test_jobs = [
        {
            "position": "DevOps Engineer",
            "company": "FunnyName Company",
            "location": "Paris",
            "jobUrl": "https://somerandomandcoolurl.com/1"
        },
        {
            "position": "Backend Kotlin Developer",
            "jobUrl": "https://somerandomandcoolurl.com/2"
        }
    ]
    
    jobs_json = json.dumps(test_jobs)
    
    result = tool._run(jobs_json)
    
    # check return message
    assert "Excel file generated" in result

    filename = result.split(": ")[1].split(" with")[0]
    
    # check if file exists
    assert os.path.exists(filename)
    
    # check content
    df = pd.read_excel(filename, keep_default_na=False)
    assert len(df) == 2
    # check if status colum is created
    assert 'status' in df.columns
    # check if missing fields are filled with "N/A"'
    assert df.iloc[1]['company'] == 'N/A'
    
    if os.path.exists(filename):
        os.remove(filename)