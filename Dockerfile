# Dockerfile for building and running the FastAPI application

FROM python:3.11-slim

# Set the working directory inside the container
WORKDIR /main

# Copy project files into the container
COPY . /main

# Install project dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for external access
EXPOSE 8000

# Command to run the application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
