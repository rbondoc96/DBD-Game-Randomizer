# Base Python image from Docker
FROM python:3.8-buster

# Set default environment variables
ENV PYTHONUNBUFFERED 1

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    tzdata \
    python3-setuptools \
    python3-pip \
    python3-dev \
    python3-venv \
    git \
    && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create and Set Working Directory
RUN mkdir /server
WORKDIR /server

COPY requirements.txt /server/
RUN pip install -r requirements.txt

# Add current directory contents to working directory
ADD . /server/