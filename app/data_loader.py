import json
from typing import List, Dict

def load_employees(filepath: str) -> List[Dict]:
    """Loads employee data from a JSON file."""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data['employees']

def format_employee_for_embedding(employee: Dict) -> str:
    """Formats a single employee's data into a single string for embedding."""
    project_str = ", ".join(employee['projects'])
    skills_str = ", ".join(employee['skills'])
    return (
        f"Name: {employee['name']}. "
        f"Experience: {employee['experience_years']} years. "
        f"Skills: {skills_str}. "
        f"Past Projects: {project_str}. "
        f"Current Status: {employee['availability']}."
    )