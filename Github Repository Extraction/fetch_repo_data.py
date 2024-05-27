import requests
import csv
import re
from bs4 import BeautifulSoup
import base64
import time
from urllib.parse import quote
from requests.adapters import HTTPAdapter

TOKEN = 'your_token'

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}
session = requests.Session()
MAX_README_LENGTH = 10000

def get_readme_content(repo_full_name):
    url = f'https://api.github.com/repos/{repo_full_name}/readme'
    response = session.get(url, headers=headers)
    response.raise_for_status()
    readme_data = response.json()
    readme_content = base64.b64decode(readme_data['content']).decode('utf-8')
    return readme_content

def clean_readme_content(content):
    soup = BeautifulSoup(content, 'html.parser')
    text = soup.get_text()

    # Remove images (markdown image syntax: ![alt text](url))
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

    # Remove URLs
    text = re.sub(r'http\S+', '', text)

    # Remove emojis and other non-text characters
    text = re.sub(r'[^\x00-\x7F]+', '', text)

    # Remove extra whitespace
    text = ' '.join(text.split())
    
    return text

def get_top_repositories(language, start_index=50, per_page=10):
    url = 'https://api.github.com/search/repositories'
    params = {
        'q': f'language:{quote(language)}',
        'sort': 'stars',
        'order': 'desc',
        'per_page': per_page,
        'page': start_index // per_page + 1
    }
    response = session.get(url, headers=headers, params=params)
    response.raise_for_status()
    repositories = response.json()['items']
    start = start_index % per_page
    return repositories[start:start + per_page]

def get_repository_languages(repo):
    url = repo['languages_url']
    response = session.get(url, headers=headers)
    response.raise_for_status()
    languages = response.json()
    top_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)[:3]
    return [lang for lang, _ in top_languages]

def get_repository_topics(repo):
    url = repo['url'] + '/topics'
    response = session.get(url, headers=headers)
    response.raise_for_status()
    topics = response.json()['names']
    return topics[:5]

csv_file = 'github_repos.csv'

languages = [
  {"urlParam": "css", "name": "CSS"},
  {"urlParam": "kotlin", "name": "Kotlin"},
  {"urlParam": "dart", "name": "Dart"},
  {"urlParam": "rust", "name": "Rust"},
  {"urlParam": "java", "name": "Java"},
  {"urlParam": "javascript", "name": "JavaScript"},
  {"urlParam": "html", "name": "HTML"},
  {"urlParam": "go", "name": "Go"},
  {"urlParam": "c", "name": "C"},
  {"urlParam": "c%2B%2B", "name": "C++"},
  {"urlParam": "python", "name": "Python"}
]

with open(csv_file, mode='w', newline='', encoding='utf-8') as output_file:
    fieldnames = ['name', 'full_name', 'stars', 'forks', 'languages', 'topics', 'readme']
    writer = csv.DictWriter(output_file, fieldnames=fieldnames)
    writer.writeheader()

    for lang in languages:
        print(f"Fetching top repositories for {lang['name']}")
        try:
            repositories = get_top_repositories(lang['urlParam'])
            for repo in repositories:
                repo_full_name = repo['full_name']
                repo_data = {
                    'name': repo['name'],
                    'full_name': repo['full_name'],
                    'stars': repo['stargazers_count'],
                    'forks': repo['forks_count'],
                    'languages': get_repository_languages(repo),
                    'topics': get_repository_topics(repo)
                }
                try:
                    readme_content = get_readme_content(repo_full_name)
                    cleaned_readme_content = clean_readme_content(readme_content)
                    if len(cleaned_readme_content) > MAX_README_LENGTH:
                        cleaned_readme_content = cleaned_readme_content[:MAX_README_LENGTH] + '... [TRUNCATED]'
                    repo_data['readme'] = cleaned_readme_content
                except requests.exceptions.RequestException as e:
                    print(f"Error fetching README for {repo_full_name}: {e}")
                    repo_data['readme'] = ''
                
                writer.writerow(repo_data)
                print(repo_data)
        except requests.exceptions.RequestException as e:
            print(f"Error fetching repositories for {lang['name']}: {e}")

print(f'Data saved to {csv_file}')
