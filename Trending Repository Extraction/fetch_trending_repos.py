import requests
import csv
import json
import time
from random import sample

with open('languages.json') as f:
    languages = json.load(f)

with open('spoken-languages.json') as f:
    spoken_languages = json.load(f)

SERVER_URL = 'https://api.gitterapp.com'

def build_url(base_url, params=None):
    if params is None:
        params = {}
    query_string = '&'.join(f"{key}={value}" for key, value in params.items() if value)
    return f"{base_url}?{query_string}" if query_string else base_url

def fetch_repositories(params):
    url = build_url(f"{SERVER_URL}/repositories", params)
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch repositories: {response.status_code}")
    return response.json()

def fetch_trending_repositories_for_languages(since):
    trending_repositories = []

    for language in languages:
        for spoken_language in spoken_languages:
            params = {
                'language': language['urlParam'],
                'spoken_language': spoken_language['urlParam'],
                'since': since
            }
            try:
                repositories = fetch_repositories(params)
                for repo in repositories:
                    repo_data = {
                        'author': repo.get('author'),
                        'name': repo.get('name'),
                        'url': repo.get('url'),
                        'description': repo.get('description'),
                        'language': language['name'],
                        'spoken_language': spoken_language['name'],
                        'stars': repo.get('stars')
                    }
                    trending_repositories.append(repo_data)
                time.sleep(1) 
            except Exception as e:
                print(f"Error fetching repositories for {language['name']} and {spoken_language['name']}: {e}")

    return trending_repositories

def save_repositories_to_csv(repositories, filename):
    try:
        fields = ['author', 'name', 'url', 'description', 'language', 'spoken_language', 'stars']
        with open(filename, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for repo in repositories:
                writer.writerow(repo)
        print(f"Data saved to {filename}")
    except Exception as e:
        print(f"Error saving repositories to CSV: {e}")
        raise

def main():
    try:
        since = 'weekly' 
        trending_repositories = fetch_trending_repositories_for_languages(since)
        save_repositories_to_csv(trending_repositories, 'trending_repos.csv')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
