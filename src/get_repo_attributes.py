import requests

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
    while True:
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