from pydantic import BaseModel
import os
import json


def generate_report(topic, client):

    class ReportGeneration(BaseModel):
        report: str
        sources: list[str]

    prompts = open("output_files/output_prompts.txt", "r").readlines()
    reports = []
    for prompt in prompts:
        prompt = prompt.strip()
        if prompt and prompt[0].isdigit():
            i = 0
            while i < len(prompt) and (prompt[i].isdigit() or prompt[i] in '. '):
                i += 1
            prompt = "Question: " + prompt[i:].strip()
            print(f"Generating report for {topic} with prompt: {prompt}")
        completion = client.beta.chat.completions.parse(
            model="gpt-4o-2024-08-06",
            messages=[
                {"role": "system", "content": "You are a Report Generation GPT. Generate a report on the given prompt. Remember the focus is on the {topic}."},
                {"role": "user", "content": "Generate a report on the following prompt: " + prompt},
            ],
            response_format=ReportGeneration,
        )

        report_generation = completion.choices[0].message.parsed
        reports.append({
            "topic": topic,
            "prompt": prompt,
            "report": report_generation.report,
            "sources": report_generation.sources
        })

    existing_reports = []
    if os.path.exists("output_files/reports.json"):
        with open("output_files/reports.json", "r") as f:
            try:
                existing_reports = json.load(f)
            except json.JSONDecodeError:
                existing_reports = []

    all_reports = existing_reports + reports

    with open("output_files/reports.json", "w") as f:
        json.dump(all_reports, f, indent=4)

