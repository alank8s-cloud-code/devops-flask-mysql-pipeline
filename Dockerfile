# BASE IMAGE

FROM python:3.12-slim

# UPGRADE SYSTEM PACKAGES (Fixes the OpenSSL CVE)

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/list/* 

# SET THE WORKING DIRECTORY INSIDE CONTAINER

WORKDIR /app

# COPY THE DEPENDENCIES

COPY requirements.txt .

# INSTALL THE DEPENDENCIES

RUN pip install --no-cache-dir -r requirements.txt 

# COPY THE REST OF THE CODE

COPY . .

# RUN THE APPLICATION

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]

