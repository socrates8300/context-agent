import re

def parse_markdown_tasks(markdown_content: str) -> list[dict]:
    """
    Parses markdown content containing a task list into a structured list of dictionaries.
    Each dictionary represents a task with its properties.
    """
    tasks = []
    task_pattern = re.compile(r'^- \[x ]\] \*\*(.*?):\*\*\s*(.*?)(?=\n- \[|

)', re.DOTALL)
    property_pattern = re.compile(r'^\s*-\s*(Context|Dependencies|Priority|Focus):\s*(.*)$', re.MULTILINE)

    matches = task_pattern.finditer(markdown_content)

    for match in matches:
        title = match.group(1).strip()
        description_and_properties = match.group(2).strip()

        task = {
            "title": title,
            "description": "",
            "context": [],
            "dependencies": [],
            "priority": "medium",
            "focus": ""
        }

        # Extract description (lines before the first property)
        lines = description_and_properties.split('\n')
        desc_lines = []
        property_found = False
        for line in lines:
            if property_pattern.match(line):
                property_found = True
                break
            desc_lines.append(line.strip())
        task["description"] = " ".join(desc_lines).strip()

        # Extract properties
        for prop_match in property_pattern.finditer(description_and_properties):
            prop_name = prop_match.group(1).lower()
            prop_value = prop_match.group(2).strip()

            if prop_name == "context":
                task["context"] = [f.strip() for f in prop_value.split(',') if f.strip()]
            elif prop_name == "dependencies":
                task["dependencies"] = [d.strip() for d in prop_value.split(',') if d.strip()]
            elif prop_name == "priority":
                task["priority"] = prop_value.lower()
            elif prop_name == "focus":
                task["focus"] = prop_value

        tasks.append(task)
    return tasks

if __name__ == '__main__':
    # Example Usage:
    markdown_example = """
# Phase 1: Initial Agent Setup and Core Capabilities

## Tasks

- [ ] **Task 1: Implement Markdown Task Parser**
  - Description: Develop a module to parse markdown task lists into a structured data format (e.g., JSON or Python objects).
  - Context: `trae_agent/cli.py`, `trae_agent/agent/base.py`
  - Focus: Regular expressions, markdown parsing libraries (if applicable), data structure design.
  - Dependencies: None
  - Priority: High

- [ ] **Task 2: Basic Context Gathering Mechanism**
  - Description: Create functions to read specified files and gather their content. Initially, this will be limited to explicit file paths.
  - Context: `trae_agent/tools/edit_tool.py`, `trae_agent/tools/bash_tool.py`
  - Focus: File I/O, error handling for non-existent files.
  - Dependencies: Task 1
  - Priority: High
"""
    parsed_tasks = parse_markdown_tasks(markdown_example)
    import json
    print(json.dumps(parsed_tasks, indent=2))
