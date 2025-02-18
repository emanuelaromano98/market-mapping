import json
import nbformat as nbf

def generate_markdown(topics, reports):
    # Parse the JSON string into Python objects if reports is a string
    if isinstance(reports, str):
        reports = json.loads(reports)
        
    # Create a new notebook (moved outside the topic loop)
    nb = nbf.v4.new_notebook()

    for topic in topics.split(","):
        markdown_content = f"# {topic}\n\n"

        for report in reports:
            if report['topic'] == topic:
                markdown_content += f"## {report['prompt'].strip()}\n\n"
                markdown_content += f"{report['report']}\n\n"
                if report['sources']:
                    markdown_content += "### Sources\n"
                    for source in report['sources']:
                        markdown_content += f"- {source}\n"
                    markdown_content += "\n"

        with open("output_files/report.md", "a") as f:
            f.write("\n" + markdown_content)
    
        # Split the markdown content into sections
        sections = markdown_content.split('\n\n')

        # Create markdown cells for each section
        for section in sections:
            if section.strip():  # Only add non-empty sections
                cell = nbf.v4.new_markdown_cell(section)
                nb.cells.append(cell)

    # Write the notebook to a file (moved outside the topic loop)
    with open("output_files/report.ipynb", "w") as f:
        nbf.write(nb, f)

