from source_files.report_generation import generate_report
from source_files.markdown_generation import generate_markdown
from source_files.prompt_generation import generate_prompt
from source_files.text_similarity_filter import filter_reports
from dotenv import load_dotenv
import os
from openai import OpenAI

def clear_output_files(file_paths):
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)

os.makedirs('output_files', exist_ok=True)

file_paths = [
    "output_files/reports.json",
    "output_files/report.ipynb",
    "output_files/report.md",
    "output_files/output_prompts.txt"
]

clear_output_files(file_paths)


industry = input("Enter the industry: ")
topics = input("Enter the topics (separated by commas): ")


load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


for topic in topics.split(","):
    print(f"Generating prompts for {topic}")
    generate_prompt(industry, topic, client)
    print(f"Generating report for {topic}")
    generate_report(topic, client)
    print(f"Finished {topic}")
    print("--------------------------------")

filter_reports()

try:
    with open("output_files/reports.json", "r") as f:
        reports = f.read()
    if not reports:
        print("No reports generated")
        exit()
except FileNotFoundError:
    print("No reports generated") 
    exit()

generate_markdown(topics, reports)
