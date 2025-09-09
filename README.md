[![PyPI version](https://badge.fury.io/py/refine_task_with_llm.svg)](https://badge.fury.io/py/refine_task_with_llm)  
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)  
[![Downloads](https://static.pepy.tech/badge/refine_task_with_llm)](https://pepy.tech/project/refine_task_with_llm)  
[![LinkedIn](https://img.shields.io/badge/LinkedIn-blue)](https://www.linkedin.com/in/eugene-evstafev-716669181/)  
  
# refine_task_with_llm  
  
`refine_task_with_llm` is a Python package that provides a function to convert loose user briefs into structured, implementation-ready task descriptions formatted in strict JSON. It leverages language models with robust extraction techniques to ensure precise, usable output for software engineering tasks.  
  
## Installation  
  
Install via pip:  
  
```bash  
pip install refine_task_with_llm  
```  
  
## Usage  
  
The main function, `refine_task_with_llm`, accepts an LLM instance and a raw user brief to return a structured JSON object describing the refined task. If no LLM is provided, it initializes a deterministic `ChatLLM7`. The function employs `llmatch` for reliable extraction of JSON from LLM output, raising errors if extraction or parsing fails.  
  
### Example  
  
```python  
from langchain_core.language_models import BaseChatModel  
from refine_task_with_llm import refine_task_with_llm  
  
# Optional: create your own LLM or pass None to use default  
result = refine_task_with_llm(  
    llm=None,  
    custom_text="Create a script to analyze sales data and generate a report.",  
    project_name="SalesAnalysis",  
    audience="junior developer",  
    include_examples=True  
)  
  
print(result)  
```  
  
This call refines an unstructured brief into a detailed, JSON-formatted task description suitable for implementation.  
  
## Author  
  
Author: Eugene Evstafev <hi@eugene.plus>  
Repository: https://github.com/chigwell/refine_task_with_llm