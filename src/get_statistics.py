import requests
import time
import get_repo_attributes as gra

# basic setting for GitHub api
GITHUB_API_URL = "https://api.github.com"
ORG_NAME = "Kaggle"
GITHUB_TOKEN = "your_github_token"
HEADERS = {
    "Accept": "application/vnd.github.v3+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}"
}

def get_repositories(org_name):
    """
    Get all repositories in Kaggle
    """
    url = f"{GITHUB_API_URL}/orgs/{org_name}/repos"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch repositories for {org_name}: {response.status_code}")
    repositories = response.json()
    return repositories

def get_repository_statistics(repo_name):
    """
    Get statistics of a repository in Kaggle
    """
    ret_stat = {}
    url = f"{GITHUB_API_URL}/repos/{ORG_NAME}/{repo_name}"
    response = requests.get(url, headers=HEADERS)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return ret_stat
    statistics = response.json()
    ret_stat["commits"] = gra.get_repository_attributes(GITHUB_API_URL, ORG_NAME, repo_name, "commits", HEADERS, 1, 500)
    ret_stat["stars"] = statistics["stargazers_count"]
    ret_stat["contributors"] = gra.get_repository_attributes(GITHUB_API_URL, ORG_NAME, repo_name, "contributors", HEADERS)
    ret_stat["branches"] = gra.get_repository_attributes(GITHUB_API_URL, ORG_NAME, repo_name, "branches", HEADERS)
    ret_stat["tags"] = gra.get_repository_attributes(GITHUB_API_URL, ORG_NAME, repo_name, "tags", HEADERS)
    ret_stat["forks"] = statistics["forks_count"]
    ret_stat["releases"] = gra.get_repository_attributes(GITHUB_API_URL, ORG_NAME, repo_name, "releases", HEADERS)
    ret_stat["closed_issues"] = gra.get_repository_attributes(GITHUB_API_URL, ORG_NAME, repo_name, "closed_issues", HEADERS) #TODO: numbers wrong
    ret_stat["environments"] = gra.get_repository_attributes(GITHUB_API_URL, ORG_NAME, repo_name, "environments", HEADERS)
    return ret_stat

def get_statistics():
    """
    Get statistics of repositories in Kaggle"
    """
    # Get all repositories in Kaggle
    repositories = get_repositories(ORG_NAME)

    # Get statistics of each repository
    for repository in repositories:
        repository_name = repository["name"]
        # repository_name = "docker-python"
        print(f"====================== Repository: {repository_name} ======================")
        statistics = get_repository_statistics(repository_name)
        print(statistics)

if __name__ == "__main__":
    #TODO: add command line arguments
    get_statistics()