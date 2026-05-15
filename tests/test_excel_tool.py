import pytest
import json
import os
import pandas as pd
from src.tools.excel_tool import ExcelExportTool
from openpyxl import load_workbook

def test_excel_export_creates_file_and_checks_columns():
    # check if the tool creat an excel file with correct content"""
    tool = ExcelExportTool()
    
    test_jobs = [
        {
            "position": "DevOps Engineer",
            "company": "FunnyName Company",
            "location": "Paris",
            "jobUrl": "https://somerandomandcoolurl.com/1",
            "companyLogo": "http://logo.com"
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
    assert len(df.columns) == 7

    # check if status colum is created
    assert 'status' in df.columns
    
    # check if the tool drops unwanted columns
    assert 'position' not in df.columns
    assert 'joburl' not in df.columns
    assert 'companylogo' not in df.columns

    # checj if new columns are created with correct data
    assert 'title' in df.columns
    assert df.iloc[0]['title'] == "DevOps Engineer"
    assert df.iloc[0]['url'] == "https://somerandomandcoolurl.com/1"

    # check if the columns were deleted
    assert 'position' not in df.columns
    assert 'companylogo' not in df.columns

    # check if missing fields are filled with "N/A"'
    assert df.iloc[1]['company'] == 'N/A'
    
    if os.path.exists(filename):
        os.remove(filename)

def test_excel_conditional_formatting_rules():
    # check if the tool applies conditional formatting rules to the "status" column

    tool = ExcelExportTool()
    test_jobs = [{"position": "DevOps", "company": "FunnyName Company", "location": "Paris", "jobUrl": "url"}]
    result = tool._run(json.dumps(test_jobs))
    filename = result.split(": ")[1].split(" with")[0]

    wb = load_workbook(filename)
    ws = wb.active

    assert len(ws.conditional_formatting) > 0

    rules_found = []
    for cf in ws.conditional_formatting:
        for rule in cf.rules:
            rules_found.append(rule.formula[0])

    assert '"Applied"' in rules_found
    assert '"Not applied"' in rules_found

    if os.path.exists(filename):
        os.remove(filename)