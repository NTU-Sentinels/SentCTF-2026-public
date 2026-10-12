# Use an official lightweight Python image
FROM python:3.11-slim

# Install system dependencies (needed if relying on standard binary libraries)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*
    
# Set the working directory inside the container
WORKDIR /app

# Copy the server script into the container
COPY Hidden_In_Plain_Sight.py .

# Expose port 8000 for network access
EXPOSE 8000

# Run the server script
CMD ["python", "Hidden_In_Plain_Sight.py"]