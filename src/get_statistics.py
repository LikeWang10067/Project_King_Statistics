import requests
import time

# basic setting for GitHub api
GITHUB_API_URL = "https://api.github.com"
ORG_NAME = "Kaggle"
ATTRIBUTE_LIST = ["commits", "stars", "contributors", "branches", "tags", "forks", "releases", "closed_issues", "environments"]
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

def get_repository_attributes(github_api_url, org_name, repo_name, info, headers, page=1, per_page=100):
    """
    Get any valid attributes of a repository
    """
    #TODO: try to do this without pagination, is there a way to get all attributes in one request?
    # similar to github user experience, where they can see the number of commits in the main page
    url = f"{github_api_url}/repos/{org_name}/{repo_name}/{info}"
    if info == "closed_issues":
        url = f"{github_api_url}/repos/{org_name}/{repo_name}/issues?state=closed"
    attributes_count = 0
    while page < 10000: # avoid very large number causing loop for a very long time
        response = requests.get(url, params={"page": page, "per_page": per_page}, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch {info} for {repo_name}: {response.status_code}")
        attributes = response.json()
        if info == "environments":
            attributes_count = attributes["total_count"]
            break
        if len(attributes) == 0:
            break
        attributes_count += len(attributes)
        page += 1
    return attributes_count

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
    attributes_list = ATTRIBUTE_LIST
    for attribute in attributes_list:
        if attribute == "commits":
            ret_stat[attribute] = get_repository_attributes(GITHUB_API_URL, ORG_NAME, repo_name, "commits", HEADERS, 1, 500)
        elif attribute == "stars":
            ret_stat[attribute] = statistics["stargazers_count"]
        elif attribute == "forks":
            ret_stat[attribute] = statistics["forks_count"]
        else:
            ret_stat[attribute] = get_repository_attributes(GITHUB_API_URL, ORG_NAME, repo_name, attribute, HEADERS)
    #TODO: closed_issue numbers wrong
    return ret_stat

def get_statistics():
    """
    Get statistics of repositories in Kaggle"
    """
    # Get all repositories in Kaggle
    repositories = get_repositories(ORG_NAME)
    raw_data = {}
    pure_data = {}

    # Get statistics of each repository
    for repository in repositories:
        repository_name = repository["name"]
        # repository_name = "docker-python"
        print(f"====================== Repository: {repository_name} ======================")
        statistics = get_repository_statistics(repository_name)

if __name__ == "__main__":
    #TODO: add command line arguments
    get_statistics()