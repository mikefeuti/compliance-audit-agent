# 1. Use a lightweight, official Python image
FROM python:3.10-slim

# 2. Set environment variables
# Prevents Python from writing pyc files to disc
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout and stderr (crucial for Cloud Logging)
ENV PYTHONUNBUFFERED=1

# 3. Set work directory
WORKDIR /app

# 4. Install dependencies
# We copy just requirements.txt first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 5. Copy the application code
COPY . .

# 6. Expose the port (Cloud Run defaults to 8080)
EXPOSE 8080

# 7. Run the application
# We use host 0.0.0.0 so it's accessible outside the container
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8080"]