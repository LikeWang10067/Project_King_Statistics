import requests

def get_repository_commits(repo_name, github_api_url, org_name):
    """
    Get commits of a repository in Kaggle
    """
    #TODO: try to do this without pagination, is there a way to get all commits in one request?
    # similar to github user experience, where they can see the number of commits in the main page
    url = f"{github_api_url}/repos/{org_name}/{repo_name}/commits"
    commits_count = 0
    page = 1
    while True:
        response = requests.get(url, params={"page": page})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch commits for {repo_name}: {response.status_code}")
        commits = response.json()
        if len(commits) == 0: # meaning we reach the end of the page
            break
        commits_count += len(commits)
        page += 1

    return commits_count