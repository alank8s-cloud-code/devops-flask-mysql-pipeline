# BASE IMAGE
FROM python:3.11-slim

# UPGRADE SYSTEM PACKAGES (fixes OpenSSL CVE)
RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# CREATE WORKING DIRECTORY
WORKDIR /app

# COPY THE CODE
COPY . .

# INSTALL PYTHON DEPENDENCIES
RUN pip install --no-cache-dir -r requirements.txt

# EXPOSE PORT
EXPOSE 5000

# SERVE THE APPLICATION
CMD ["python", "app.py"]