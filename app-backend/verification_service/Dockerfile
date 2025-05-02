FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /verification_service

# Copy the content from the local verification_service directory to the container
COPY . .

# Install the required dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run fastapi when the container launches
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]