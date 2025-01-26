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
- [License](#license)

## Installation

### Prerequisites
- Python 3.x
- Docker (for Task 3)

## Task 1 & 2: Google Colab Setup

### Step 1: Set up Google Colab environment
1. Go to [Google Colab](https://colab.research.google.com/).
2. Create a new notebook.

### Step 2: Install required libraries
```python
!pip install scikit-learn pandas numpy
!pip install nltk
