import requests
import os
from collections import Counter

GITHUB_API = "https://api.github.com"
USERNAME = os.environ["GITHUB_USERNAME"]
TOKEN = os.environ["GITHUB_TOKEN"]

headers = {
    "Authorization": f"token {TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def get_repositories(username):
    repos = []
    page = 1
    while True:
        url = f"{GITHUB_API}/users/{username}/repos?per_page=100&page={page}"
        response = requests.get(url, headers=headers)
        data = response.json()
        if not data:
            break
        repos.extend(data)
        page += 1
    return repos

def get_languages(repo_full_name):
    url = f"{GITHUB_API}/repos/{repo_full_name}/languages"
    response = requests.get(url, headers=headers)
    return response.json()

def update_readme(languages):
    start_tag = "<!-- LANGUAGES-START -->"
    end_tag = "<!-- LANGUAGES-END -->"

    with open("README.md", "r", encoding="utf-8") as f:
        content = f.read()

    before = content.split(start_tag)[0]
    after = content.split(end_tag)[-1]

    middle = "\n".join(f"- **{lang}**: {bytes_count} bytes" for lang, bytes_count in languages)

    new_content = f"{before}{start_tag}\n{middle}\n{end_tag}{after}"

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(new_content)

def main():
    repos = get_repositories(USERNAME)
    language_counter = Counter()

    for repo in repos:
        if repo.get("fork"):
            continue
        languages = get_languages(repo["full_name"])
        for lang, count in languages.items():
            language_counter[lang] += count

    sorted_languages = language_counter.most_common()
    update_readme(sorted_languages)

if __name__ == "__main__":
    main()
