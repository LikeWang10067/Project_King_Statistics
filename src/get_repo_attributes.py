import requests

def get_repository_commits(repo_name, github_api_url, org_name):
    """
    Get commits of a repository
    """
    #TODO: try to do this without pagination, is there a way to get all commits in one request?
    # similar to github user experience, where they can see the number of commits in the main page
    url = f"{github_api_url}/repos/{org_name}/{repo_name}/commits"
    commits_count = 0
    page = 1
    while True:
        response = requests.get(url, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch commits for {repo_name}: {response.status_code}")
        commits = response.json()
        if len(commits) == 0: # meaning we reach the end of the page
            break
        commits_count += len(commits)
        page += 1
    return commits_count

def get_repository_contributors(repo_name, github_api_url, org_name):
    """
    Get contributors of a repository
    """
    #TODO: try to do this without pagination, same as above
    url = f"{github_api_url}/repos/{org_name}/{repo_name}/contributors"
    contributors_count = 0
    page = 1
    while True:
        response = requests.get(url, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch contributors for {repo_name}: {response.status_code}")
        contributors = response.json()
        if len(contributors) == 0: # meaning we reach the end of the page
            break
        contributors_count += len(contributors)
        page += 1
    return contributors_count

def get_repository_branches(repo_name, github_api_url, org_name):
    """
    Get branches of a repository
    """
    url = f"{github_api_url}/repos/{org_name}/{repo_name}/branches"
    branches_count = 0
    page = 1
    while True:
        response = requests.get(url, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch branches for {repo_name}: {response.status_code}")
        branches = response.json()
        if len(branches) == 0: # meaning we reach the end of the page
            break
        branches_count += len(branches)
        page += 1
    return branches_count

def get_repository_tags(repo_name, github_api_url, org_name):
    """
    Get tags of a repository
    """
    url = f"{github_api_url}/repos/{org_name}/{repo_name}/tags"
    tags_count = 0
    page = 1
    while True:
        response = requests.get(url, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch tags for {repo_name}: {response.status_code}")
        tags = response.json()
        if len(tags) == 0: # meaning we reach the end of the page
            break
        tags_count += len(tags)
        page += 1
    return tags_count

def get_repository_releases(repo_name, github_api_url, org_name):
    """
    Get releases of a repository
    """
    url = f"{github_api_url}/repos/{org_name}/{repo_name}/releases"
    releases_count = 0
    page = 1
    while True:
        response = requests.get(url, params={"page": page, "per_page": 100})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch releases for {repo_name}: {response.status_code}")
        releases = response.json()
        if len(releases) == 0: # meaning we reach the end of the page
            break
        releases_count += len(releases)
        page += 1
    return releases_count

def get_repository_closed_issues(repo_name, github_api_url, org_name):
    """
    Get closed issues of a repository
    """
    url = f"{github_api_url}/repos/{org_name}/{repo_name}/issues"
    closed_issues_count = 0
    page = 1
    while True:
        response = requests.get(url, params={"page": page, "per_page": 100, "state": "closed"})
        if response.status_code != 200:
            raise Exception(f"Failed to fetch closed issues for {repo_name}: {response.status_code}")
        issues = response.json()
        if len(issues) == 0: # meaning we reach the end of the page
            break
        closed_issues_count += len(issues)
        page += 1
    return closed_issues_count

def get_repository_environments(repo_name, github_api_url, org_name):
    """
    Get environments of a repository
    """
    url = f"{github_api_url}/repos/{org_name}/{repo_name}/environments"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch environments for {repo_name}: {response.status_code}")
    environments = response.json()
    environments_count = environments["total_count"]
    return environments_count
    # environments_count = 0
    # page = 1
    # while True:
    #     response = requests.get(url, params={"page": page})
    #     if response.status_code != 200:
    #         raise Exception(f"Failed to fetch environments for {repo_name}: {response.status_code}")
    #     environments = response.json()
    #     if len(environments) == 0: # meaning we reach the end of the page
    #         break
    #     environments_count += len(environments)
    #     page += 1
    # return environments_count