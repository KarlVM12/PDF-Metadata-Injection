# PDF Metadata Injector

Add any extra context, keywords, etc. into the metadata of any PDF

### How to use
1. Create a venv and install dependencies
2. Call the file:
```
# If you want to enter all on the command line:
python add_pdf_metadata.py resume.pdf resume_with_keywords.pdf \
  --title "Resume - Software Engineer" \
  --author "Your Name" \
  --subject "Job Application - Backend" \
  --keywords "Python, SQL, REST APIs, AWS, Docker, CI/CD, Postgres"

# Load keywords from a text file (one per line or comma-separated):
python add_pdf_metadata.py resume.pdf resume_with_keywords.pdf \
  --keywords-file job_keywords.txt

# To overwrite an existing output file:
python add_pdf_metadata.py resume.pdf resume.pdf --keywords "Python, SQL" --overwrite

```
