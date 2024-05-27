import requests
import csv
import base64
import re
from bs4 import BeautifulSoup

GITHUB_API_URL = 'https://api.github.com'
CSV_INPUT_FILE = 'trending_repos.csv'
CSV_OUTPUT_FILE = 'trending_metadata.csv'

GITHUB_TOKEN = 'your_token' 
headers = {'Authorization': f'token {GITHUB_TOKEN}'} if GITHUB_TOKEN else {}

MAX_README_LENGTH = 10000

def get_readme_content(repo_full_name):
    url = f'{GITHUB_API_URL}/repos/{repo_full_name}/readme'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    readme_data = response.json()
    readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
    return readme_content

def clean_readme_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()

    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

    text = re.sub(r'http\S+', '', text)

    text = re.sub(r'[^\x00-\x7F]+', '', text)

    text = ' '.join(text.split())
    
    return text

def get_repository_languages(repo_full_name):
    url = f'{GITHUB_API_URL}/repos/{repo_full_name}/languages'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    languages = response.json()
    top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]
    return [lang for lang, _ in top_languages]

def get_repository_topics(repo_full_name):
    url = f'{GITHUB_API_URL}/repos/{repo_full_name}/topics'
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    topics = response.json().get('names', [])
    return topics[:5]

with open(CSV_INPUT_FILE, mode='r', newline='', encoding='utf-8') as input_file:
    reader = csv.DictReader(input_file)
    repos = [row for row in reader]

with open(CSV_OUTPUT_FILE, mode='w', newline='', encoding='utf-8') as output_file:
    fieldnames = ['author', 'name', 'url', 'description', 'language', 'spoken_language', 'stars', 'languages', 'topics', 'readme']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()
    for repo in repos:
        repo_full_name = f"{repo['author']}/{repo['name']}"
        repo_data = {
            'author': repo['author'],
            'name': repo['name'],
            'url': repo['url'],
            'description': repo['description'],
            'language': repo['language'],
            'spoken_language': repo['spoken_language'],
            'stars': repo['stars'],
            'languages': [],
            'topics': [],
            'readme': ''
        }
        try:
            repo_data['languages'] = get_repository_languages(repo_full_name)
            repo_data['topics'] = get_repository_topics(repo_full_name)
            readme_content = get_readme_content(repo_full_name)
            cleaned_readme_content = clean_readme_content(readme_content)
            if len(cleaned_readme_content) > MAX_README_LENGTH:
                cleaned_readme_content = cleaned_readme_content[:MAX_README_LENGTH] + '... [TRUNCATED]'
            repo_data['readme'] = cleaned_readme_content
        except requests.exceptions.RequestException as e:
            print(f"Error fetching data for {repo_full_name}: {e}")
        
        writer.writerow(repo_data)
        print(repo_data)

print(f'Data saved to {CSV_OUTPUT_FILE}')
