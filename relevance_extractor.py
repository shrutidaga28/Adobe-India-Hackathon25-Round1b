import os
import json
import fitz  # PyMuPDF
from datetime import datetime
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Paths
INPUT_DIR = "input"
OUTPUT_DIR = "output"

# Read persona + job descriptions
with open("persona.txt", "r", encoding="utf-8") as f:
    persona = f.read().strip()

with open("job.txt", "r", encoding="utf-8") as f:
    job = f.read().strip()

# Combine both into a single query
query = persona + " " + job

# Final Output Format
formatted_output = {
    "metadata": {
        "input_documents": [],
        "persona": persona,
        "job_to_be_done": job,
        "processing_timestamp": datetime.now().isoformat()
    },
    "extracted_sections": [],
    "sub_section_analysis": []
}

# Go through each PDF in input folder
for filename in os.listdir(INPUT_DIR):
    if filename.endswith(".pdf"):
        doc_path = os.path.join(INPUT_DIR, filename)
        doc = fitz.open(doc_path)

        page_texts = []
        page_mapping = []

        # Extract text from each page
        for i, page in enumerate(doc, start=1):
            text = page.get_text().strip()
            if len(text) > 30:
                page_texts.append(text)
                page_mapping.append(i)

        # TF-IDF + Cosine Similarity
        tfidf = TfidfVectorizer(stop_words="english")
        vectors = tfidf.fit_transform([query] + page_texts)
        similarities = cosine_similarity(vectors[0:1], vectors[1:])[0]

        # Get Top 3 relevant pages
        top_indices = similarities.argsort()[-3:][::-1]

        # Add filename to metadata
        formatted_output["metadata"]["input_documents"].append(filename)

        for rank, idx in enumerate(top_indices, start=1):
            raw_text = page_texts[idx].strip()
            refined_text = raw_text[:500] + "..." if len(raw_text) > 500 else raw_text
            page_num = page_mapping[idx]
            score = round(float(similarities[idx]), 3)

            # Extracted Section Entry
            formatted_output["extracted_sections"].append({
                "document": filename,
                "page_number": page_num,
                "section_title": refined_text[:40].replace("\n", " ") + "...",
                "importance_rank": rank
            })

            # Sub-section Analysis Entry
            formatted_output["sub_section_analysis"].append({
                "document": filename,
                "refined_text": refined_text,
                "page_number": page_num
            })

# Save the final output
os.makedirs(OUTPUT_DIR, exist_ok=True)
final_output_path = os.path.join(OUTPUT_DIR, "output.json")

with open(final_output_path, "w", encoding="utf-8") as f:
    json.dump(formatted_output, f, indent=2)

print(f"✅ Final formatted output saved to: {final_output_path}")
