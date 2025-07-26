FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /rag_worker

# Copy the content from the local rag_worker directory to the container
COPY rag_worker/ .

# Copy the shared code inside the container
COPY common/ common/

# Install the required dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run python when the container launches
CMD ["python", "rabbitmq_bg.py"]