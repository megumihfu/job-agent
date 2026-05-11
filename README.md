# AI-Powered Job Hunter

An intelligent agent designed to automate the search and filtering of DevOps/Cloud & Backend Engineer roles. This project specifically targets the French and German markets, with a focus on architectural clean code and cost-optimized AI processing.

This project demonstrates full-stack automation skills, integrating external APIs with LLM intelligence to drastically reduce job board noise while maintaining high precision in criteria matching.

## **Tech Stack**

### **Logic**
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pandas](https://img.shields.io/badge/pandas-%23150458.svg?style=for-the-badge&logo=pandas&logoColor=white)

### **AI**
![CrewAI](https://img.shields.io/badge/CrewAI-000000?style=for-the-badge&logo=openai&logoColor=white)
![OpenAI](https://img.shields.io/badge/GPT--4o--mini-412991?style=for-the-badge&logo=openai&logoColor=white)

### **Tools & Export**
![LinkedIn](https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white)
![Microsoft Excel](https://img.shields.io/badge/Microsoft_Excel-217346?style=for-the-badge&logo=microsoft-excel&logoColor=white)

---

## Features
* **Multi-market search**: Automated scraping for relevant positions across France and Germany.
* **Filtering pipeline (AI Screening)**: GPT-4o-mini validation of experience limits, contract-type, salary...
* **Intelligent localization**: Context-aware geographic validation and language requirement assessment.
* **Dynamic Excel export**: Automated generation of styled reports with conditional formatting and status dropdown menus.

---

## **Getting Started**

### **Prerequisites**
Make sure you have installed:
* At least Python 3.10 
* A virtual environment tool (`venv`)

### **Running the Project**
1. **Clone the repository**
   ```bash
   git clone https://github.com/megumihfu/job-search-agent.git
   ```
   
2. **Setup virtual environment**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

3. **Install dependencies**
  ```bash
  pip install -r requirements.txt
  ```

4. **Environment variables**
   Create a `.env` file at the project root.
  ```bash
  CHATANYWHERE_API_KEY = "your_api_key_here"
  ```

5. **Execute the agent**
  ```bash
  python main.py
  ```

### **Architecture**
The project follows a modular, tool-based architecture:
* **LinkedInTool**: handles API interactions & initial data deduplication.
* **ExcelExportTool**: encapsulates the logic for data styling, Excel formatting (openpyxl), and persistence.
* **Agent logic**: implements a sequential pipeline: Fetch -> Semantic Analyze (AI) -> Export

### **Project structure**
```python
┌── src/
│   ├── agents/
│   │   └── job_agent.py      # LLM conf & prompt
│   ├── tools/
│   │   ├── linkedin_tool.py  # data acquisition
│   │   └── excel_tool.py     # export logic
│   └── config.py             # API conf
├── outputs/                  # generated excel files
├── tests/                    # unit tests
├── venv/                     # virtual env
├── main.py                   # entry point
├── requirements.txt
└── README.md
```

### Scope decisions
* **Architectural pivot (efficiency)**: Initially, the project was built using multiple autonomous CrewAI agents and tasks. However, analysis showed that the multi-agent overhead was consuming an excessive amount of tokens and increasing processing time.
* **Streamlined pipeline**: The architecture was refactored into a custom Python loop. By using a single targeted LLM call with a precise prompt, the project achieved a **60% reduction in token consumption** and significantly faster execution times without losing analysis quality.
* **Constraint handling**: default "YES" on missing data (salary/experience) to avoid false negatives.
