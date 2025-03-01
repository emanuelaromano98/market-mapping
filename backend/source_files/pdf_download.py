import markdown
from weasyprint import HTML

def convert_md_to_pdf(md_file, pdf_file):
    with open(md_file, "r", encoding="utf-8") as f:
        md_content = f.read()

    # Convert Markdown to HTML
    html_content = markdown.markdown(md_content)

    # Convert HTML to PDF
    HTML(string=html_content).write_pdf(pdf_file)

# Example usage
convert_md_to_pdf("backend/output_files/report.md", "backend/output_files/report.pdf")