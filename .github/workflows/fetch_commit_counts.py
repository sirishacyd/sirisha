import requests
import os

GITHUB_USERNAME = 'your-github-username'  # Replace with your GitHub username
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def get_repos(username):
    repos = []
    page = 1
    while True:
        url = f'https://api.github.com/users/{username}/repos?per_page=100&page={page}'
        response = requests.get(url, headers={'Authorization': f'token {GITHUB_TOKEN}'})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch repos: {response.status_code} {response.text}")
        repos.extend(response.json())
        if len(response.json()) < 100:
            break
        page += 1
    return repos

def get_commit_count(repo):
    commits = 0
    page = 1
    while True:
        url = f'https://api.github.com/repos/{repo["full_name"]}/commits?per_page=100&page={page}'
        response = requests.get(url, headers={'Authorization': f'token {GITHUB_TOKEN}'})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch commits: {response.status_code} {response.text}")
        commits += len(response.json())
        if len(response.json()) < 100:
            break
        page += 1
    return commits

def get_total_commits(username):
    repos = get_repos(username)
    total_commits = 0
    for repo in repos:
        commit_count = get_commit_count(repo)
        total_commits += commit_count
    return total_commits

if __name__ == "__main__":
    total_commits = get_total_commits(GITHUB_USERNAME)
    print(total_commits)
