import sys
import json
import os
from datetime import datetime

if len(sys.argv) != 2:
    print("Usage: python convert_output_format.py <collection_name>")
    sys.exit(1)

collection = sys.argv[1]
input_path = os.path.join(collection, "output", "results.json")
output_path = os.path.join(collection, "output", "output.json")

if not os.path.exists(input_path):
    print(f"❌ Error: {input_path} not found.")
    sys.exit(1)

with open(input_path, "r", encoding="utf-8") as f:
    data = json.load(f)

# Format output according to Adobe Challenge 1B spec
formatted_output = {
    "metadata": {
        "input_documents": [doc["filename"] for doc in data.get("documents", [])],
        "persona": data.get("persona", ""),
        "job_to_be_done": data.get("job", ""),
        "processing_timestamp": datetime.now().isoformat()
    },
    "extracted_sections": [],
    "sub_section_analysis": []
}

for doc in data.get("documents", []):
    for i, section in enumerate(doc.get("relevant_sections", [])):
        formatted_output["extracted_sections"].append({
            "document": doc["filename"],
            "page_number": section["page"],
            "section_title": section["text"][:40].strip().replace("\n", " ") + "...",
            "importance_rank": i + 1
        })

        formatted_output["sub_section_analysis"].append({
            "document": doc["filename"],
            "refined_text": section["text"].strip(),
            "page_number": section["page"]
        })

# Save the new formatted output
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(formatted_output, f, indent=2)

print(f"✅ Reformatted output saved to {output_path}")

