# GitHub Repository Recommender System 📊🚀

Welcome to the GitHub Repository Recommender System! This project is designed to fetch data from GitHub repositories, preprocess it, and use various algorithms to recommend repositories to users based on their preferences. Below is a detailed guide on how to set up, run, and understand the project.

## Table of Contents

1. [Introduction](#introduction)
2. [Features](#features)
3. [Getting Started](#getting-started)
   - [Prerequisites](#prerequisites)
   - [Installation](#installation)
4. [Pipeline Overview](#pipeline-overview)

## Introduction

This project aims to provide a robust recommender system for GitHub repositories. It involves fetching repository data, preprocessing the data, extracting relevant keywords, and generating recommendations based on similarity metrics.

## Features

- **Data Fetching**: Retrieve repository data, README content, and issues/labels from GitHub.
- **Data Preprocessing**: Clean and preprocess the fetched data.
- **Keyword Extraction**: Extract keywords using TF-IDF, LDA, and BERT.
- **Similarity Calculation**: Compute similarity between user preferences and repository features.
- **Recommendations**: Generate and display repository recommendations for users.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.7+
- Git
- Virtual Environment (optional but recommended)

### Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/your-username/github-recommender-system.git
   cd github-recommender-system
2. Install the required python packages:
   ```sh
   pip install -r requirements.txt

4. Add your github token to the enviroment:
   ```sh
   export GITHUB_TOKEN='your_github_token'

## Pipeline Overview

### Data Fetching

1. **Fetch Repository Data**: Use `fetch_repo_data.py` to gather repository metadata, README content, languages, and topics.
2. **Fetch Issue Labels**: Use `fetch_issue_labels.py` to scrape issue labels from repository pages.
3. **Fetch Trending Repositories**: Use `fetch_trending_repos.py` to get trending repositories based on language and spoken language.
4. **Fetch Trending Metadata**: Use `fetch_trending_repos_metadata.py` to gather metadata for trending repositories.
5. **Fetch Trending Issues Labels**: Use `fetch_trending_issues_labels.py` to scrape issue labels for trending repositories.

### Data Preprocessing and Keyword Extraction

1. **Preprocess Data**: Clean and preprocess the README content and issues.
2. **Extract Keywords**: Use TF-IDF, LDA, and BERT to extract relevant keywords from the README and issues.

### Similarity Index Matching

1. **Vectorize Data**: Transform the preprocessed data into vectors using TF-IDF.
2. **Compute Similarity**: Calculate cosine similarity between user preferences and repository vectors.
3. **Generate Recommendations**: Recommend repositories to users based on the highest similarity scores.

