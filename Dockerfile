# Base image
FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev ffmpeg wget unzip \
    && rm -rf /var/lib/apt/lists/*

# Create working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Download PaddleOCR models at build time (optional: can also mount in volume or pre-bundle)
# RUN wget https://paddleocr.bj.bcebos.com/PP-OCRv3/en_PP-OCRv3_rec_slim_infer.tar && \
#     tar -xvf en_PP-OCRv3_rec_slim_infer.tar -C models/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Expose port
EXPOSE 8080

# Run the FastAPI app with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
