import requests
import statistics as sta
import json

# basic setting for GitHub api
GITHUB_API_URL = "https://api.github.com"

def get_repositories(org_name, headers, page=1, per_page=100):
    """
    Get all repositories in Kaggle
    """
    url = f"{GITHUB_API_URL}/orgs/{org_name}/repos"
    repositories = []
    while True:
        params = {"page": page, "per_page": per_page}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch repositories for {org_name} on page {page}: {response.status_code}")
        repositories.extend(response.json())
        if len(response.json()) == 0:
            break
        page += 1
    return repositories

def get_repository_attributes(github_api_url, org_name, repo_name, info, headers, page=1, per_page=100):
    """
    Get any valid attributes of a repository
    """
    #TODO: try to do this without pagination, is there a way to get all attributes in one request?
    # similar to github user experience, where they can see the number of commits in the main page
    url = f"{github_api_url}/repos/{org_name}/{repo_name}/{info}"
    attributes_count = 0
    while True:
        params = {"page": page, "per_page": per_page}
        if info == "closed_issues":
            url = f"{github_api_url}/search/issues?q=repo:{org_name}/{repo_name}+is:issue+is:closed"
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Failed to fetch {info} for {repo_name}: {response.status_code}")
        attributes = response.json()
        if info == "environments":
            attributes_count = attributes["total_count"]
            break
        if info == "closed_issues":
            attributes_count = attributes["total_count"]
            break
        if len(attributes) == 0:
            break
        attributes_count += len(attributes)
        page += 1
    return attributes_count

def get_repository_statistics(org_name ,repo_name, headers, attribute_list):
    """
    Get statistics of a repository in Kaggle
    """
    ret_stat = {}
    url = f"{GITHUB_API_URL}/repos/{org_name}/{repo_name}"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return ret_stat
    statistics = response.json()
    for attribute in attribute_list:
        if attribute == "commits":
            ret_stat[attribute] = get_repository_attributes(GITHUB_API_URL, org_name, repo_name, "commits", headers, 1, 500)
        elif attribute == "stars":
            ret_stat[attribute] = statistics["stargazers_count"]
        elif attribute == "forks":
            ret_stat[attribute] = statistics["forks_count"]
        else:
            ret_stat[attribute] = get_repository_attributes(GITHUB_API_URL, org_name, repo_name, attribute, headers)
    return ret_stat

def get_statistics_report(org_name, headers, attribute_list):
    """
    Get statistics of repositories in Kaggle"
    """
    # Get all repositories in Kaggle
    repositories = get_repositories(org_name, headers)
    raw_data = {}
    pure_data = {}

    # Get statistics of each repository
    for repository in repositories:
        repository_name = repository["name"]
        print(f"====================== Repository: {repository_name} ======================")
        statistics = get_repository_statistics(org_name, repository_name, headers, attribute_list)
        print(statistics)
        raw_data[repository_name] = statistics
        for attribute in statistics:
            if attribute not in pure_data:
                pure_data[attribute] = []
            pure_data[attribute].append(statistics[attribute])
    
    # Proferm data analysis and save the results into a json file
    print("================================= Data Analysis =================================")
    statistics_results = {}
    for attribute in pure_data:
        data = pure_data[attribute]
        print(f"Attribute: {attribute}")
        # print(f"Max: {max(data)}") 
        # print(f"Min: {min(data)}")
        print(f"Total: {sum(data)}")
        print(f"Median: {sta.median(sorted(data))}")
        print(f"=================================")
        statistics_results[attribute] = {
            "total": sum(data),
            "median": sta.median(sorted(data))
        }
    with open("statistics_results.json", "w") as file_stream:
        file_stream.write(json.dumps(statistics_results, indent=4))


if __name__ == "__main__":
    import os, sys, getopt
    def usage():
        print('Usage:  ' + os.path.basename(__file__) + ' options filepath ')
        print('Options:')
        print('\t-h, --help: print basic usage information')
        print('\t-t, --token: GitHub token')
        print('\t-o, --org_name: organization name')
        print('\t-a, --attributes: attributes list')
        print('Note:')
        print('\tThe default organization name is Kaggle')
        print('\tThe default attributes list is commits,stars,contributors,branches,tags,forks,releases,closed_issues,environments')
        print('\tIf you want to change the default settings, please use -o and -a options')
        print('Example:')
        print('\t$ python get_statistics.py -t <GitHub token> -o langchain-ai -a commits,stars')
        print('\tMeaning: get statistics of commits and stars for all repositories in the organization: langchain-ai')
        sys.exit(0)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ht:o:a:", ["help", "token=", "org_name=", "attributes"])
    except getopt.GetoptError as err:
        print(err)
        usage()
    github_token = None
    org_name = "Kaggle" # default organization name
    attribute_list = ["commits", "stars", "contributors", "branches", "tags", "forks", "releases", "closed_issues", "environments"] # default attributes
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
        if opt in ("-t", "--token"):
            github_token = arg
            headers = {
                "Accept": "application/vnd.github.v3+json",
                "Authorization": f"Bearer {github_token}"
            }
        if opt in ("-o", "--org_name"):
            org_name = arg
        if opt in ("-a", "--attributes"):
            attribute_list = arg.split(",")
    # check if the token is set
    if github_token is None:
        print('GitHub token is required to avoid GitHub API rate limit')
        usage()
    get_statistics_report(org_name, headers, attribute_list)