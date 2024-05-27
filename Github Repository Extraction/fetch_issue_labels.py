import requests
import csv
import re
from bs4 import BeautifulSoup

CSV_FIELD_SIZE_LIMIT = 2147483647
csv.field_size_limit(CSV_FIELD_SIZE_LIMIT)
MAX_ISSUES_LENGTH = 10000

def scrape_labels_from_url(url):
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, 'html.parser')
    a_id_elements = soup.find_all('a', id=True)

    labels = []
    for a_id_element in a_id_elements:
        if a_id_element.span:
            label_text = a_id_element.span.text.strip()
            label_text = re.sub(r'[\n\s]+', ' ', label_text)
            if label_text:
                labels.append(label_text)

    return labels

csv_file = 'github_repos.csv'
updated_csv_file = 'github_repos_with_issues.csv'

with open(csv_file, mode='r', newline='', encoding='utf-8') as input_file:
    reader = csv.DictReader(input_file)
    fieldnames = reader.fieldnames + ['issues']

    with open(updated_csv_file, mode='w', newline='', encoding='utf-8') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            name = row['name']
            full_name = row['full_name']
            repo_url = f'https://github.com/{full_name}/labels?sort=count-desc'
            print(f"Fetching labels for {name}:")
            try:
                labels = scrape_labels_from_url(repo_url)
                issues_text = ', '.join(labels)

                # Truncate the issues text if it exceeds the maximum length
                if len(issues_text) > MAX_ISSUES_LENGTH:
                    issues_text = issues_text[:MAX_ISSUES_LENGTH] + '... [TRUNCATED]'

                row['issues'] = issues_text
                writer.writerow(row)
                print(labels)
                print()
            except requests.exceptions.RequestException as e:
                print(f"Error fetching labels for {name}: {e}")

print(f'Data saved to {updated_csv_file}')
