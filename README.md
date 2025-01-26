# NLP-pipeline-microservice
# Multi-Label Classification and Entity Extraction API

This repository contains the code for a multi-label classification and entity extraction model served via a REST API using Flask. The project is divided into three main tasks:
1. Multi-label classification model training (Google Colab).
2. Entity extraction model training (Google Colab).
3. Docker containerization of the Flask API to serve the model.

## Table of Contents
- [Installation](#installation)
- [Task 1 & 2: Google Colab Setup](#task-1--2-google-colab-setup)
- [Task 3: Docker Setup](#task-3-docker-setup)
- [API Usage](#api-usage)
- [Error Analysis](#error-analysis)


## Installation

### Prerequisites
- Python 3.x
- Docker (for Task 3)

## Task 1 & 2: Google Colab Setup

### Step 1: Set up Google Colab environment
1. Go to [Google Colab](https://colab.research.google.com/).
2. Create a new notebook.

### Step 2: Install required libraries
### Step 3. Run the codes cell-wise (Descriptions are provided in colab notebook itself).

## Task 3
### Step 1: Install Docker
Follow the Docker installation guide.
### Step 2: Make a Dockerfile and a requirements.txt file
### Step 3: Build Docker Image
```bash
docker build -t myflaskapp .
```
### Step 4: Run it
```bash
docker build -t nlp-microservice .
docker run -p 5000:5000 nlp-microservice
```
### Step 5: Curl to send POST request 
```bash
curl -X POST http://localhost:5000/predict -H "Content-Type: application/json" -d '{"text_snippet": "We love the analytics, but CompetitorX has a cheaper subscription."}'
```
### Response would look like :
```
{
  "text_snippet": "We love the analytics, but CompetitorX has a cheaper subscription.",
  "predicted_labels": ["Positive", "Pricing"],
  "extracted_entities": [
    {"type": "feature", "value": "analytics"},
    {"type": "competitor", "value": "CompetitorX"},
    {"type": "pricing", "value": "cheaper subscription"}
  ],
  "summary": "Summary: We love the analytics, but CompetitorX has..."
}
```
