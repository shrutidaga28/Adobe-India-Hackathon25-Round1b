# Base image with Python
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set default command to run your script
CMD ["python", "relevance_extractor.py"]
