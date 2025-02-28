import json
import nbformat as nbf

def generate_markdown(topics, reports):
    # Parse the JSON string into Python objects if reports is a string
    if isinstance(reports, str):
        reports = json.loads(reports)

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

