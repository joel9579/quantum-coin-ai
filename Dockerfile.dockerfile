# Base image
FROM python:3.11.1-slim

# Set work directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entire project
COPY . .

# Expose port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]
