# Challenge 1B: Persona-Based PDF Relevance Extraction
# Overview
This project extracts and ranks the most relevant sections from PDFs based on a provided persona and job description. Using NLP (TF-IDF + cosine similarity), it compares document content to the user's goal and outputs a structured JSON format.

# Folder Structure
```bash
adobe_hack_1b/
├── relevance_extractor.py           # Main Docker script (outputs results.json)
├── convert_output_format.py         # Converts results.json → formatted_output.json
├── requirements.txt                 # Python dependencies
├── Dockerfile                       # Docker image configuration
├── README.md                        # This file
├── collection_1/
│   ├── input/                       # Input PDFs
│   ├── output/                      # Output JSON files
│   ├── persona.txt
│   └── job.txt
├── collection_2/
├── collection_3/
└── collection_4/
```
Each collection contains a new test case with input PDFs, a persona, and a job file.

# How to Run
Here’s how you process a new collection folder (e.g., collection_4):

# Step 1: Place Input Files
Inside collection_4:

1. input/ → Add one or more PDF files

2. persona.txt → Add persona description

3. job.txt → Add job-to-be-done description

4. output/ → Create empty folder (Docker will write here)

# Step 2: Run Docker Command
Run this in your terminal (PowerShell or Git Bash):
```bash
docker run --rm ^
  -v "${PWD}/collection_4/input:/app/input" ^
  -v "${PWD}/collection_4/output:/app/output" ^
  -v "${PWD}/collection_4/persona.txt:/app/persona.txt" ^
  -v "${PWD}/collection_4/job.txt:/app/job.txt" ^
  --network none pdf-relevance-extractor
```

This will generate:
```bash
collection_4/output/results.json
```
But this is not in final format.

# Step 3: Convert to Final Output Format
To convert results.json to the required format (formatted_output.json), run:
```bash
python convert_output_format.py collection_4
```
This will generate:
```bash
collection_4/output/formatted_output.json
```
This formatted output follows the Adobe Hackathon expected structure with:

metadata
extracted_sections
sub-section_analysis

# Example Collection
collection_1/

1. input/: marketing_report.pdf

2. persona.txt: "A marketing manager focused on digital campaigns..."

3. job.txt: "Looking for ways to increase customer engagement..."

# Output:

output/results.json → raw output

output/formatted_output.json → final output

# Output Format Example
```bash
{
  "metadata": {
    "input_documents": ["example.pdf"],
    "persona": "A digital marketing manager...",
    "job_to_be_done": "Extract strategies for improving brand engagement...",
    "processing_timestamp": "2025-07-25T14:35:22"
  },
  "extracted_sections": [
    {
      "document": "example.pdf",
      "section_title": "Social Media Engagement Strategies",
      "importance_rank": 1,
      "page_number": 3
    }
  ],
  "subsection_analysis": [
    {
      "document": "example.pdf",
      "refined_text": "Social media campaigns improve engagement by...",
      "page_number": 3
    }
  ]
}
```

# Notes

1. Output must be generated using CPU only (no GPU)
2. Model size used is under 1GB
3. Processing time per collection ≤ 60 seconds
5. No internet access is used inside Docker
