# BASE-IMAGE

FROM python:3.11-slim

# CREATE A WORKING DIRECTORY

WORKDIR /app

# COPY THE CODE FROM REMOTE TO LOCAL

COPY . . 

RUN apt-get update && apt-get upgrade -y && rm -rf /var/lib/apt/lists/*

# INSTALLING THE PACKAGES & DEPENDENCIES

RUN pip install -r --no-cache-dir requirements.txt

# EXPOSE

EXPOSE 5000

# SERVE THE APPLICATION

CMD ["python","app.py"]
