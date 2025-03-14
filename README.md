# Project_King_Statistics

This project fetches and analyzes statistics for all repositories under a specified GitHub organization. It uses the GitHub API and cloc to retrieve repository data and generates a report with total and median values for various attributes.

---

## **Main Features**
- Fetch statistics for all repositories in a GitHub organization.
- Analyze general attributes such as commits, stars, contributors, branches, tags, forks, releases, closed issues, and environments.
- Gain special attributes: lines of code for all programming language in this repository.
- Customize the organization name and attributes to analyze. The way we analyze lines of code is a little bit different from general attributes, we will only record the data of a programming language if it has lines of code in the repository, this is to prevent having a lot of 0s when trying to get the median of a data set, I wanted to avoid having a dataset like this: `[0, 0, 0, 121, 3, 0, 0, 1, 0, 0, 0, 0]`, a more valid dataset would be like `[121, 3, 1]`.
- Generate a report (.json file) with total and median values for the selected attributes.

---

### **Command-Line Options**
The script supports the following command-line options:

| Option            | Description                                                                 |
|-------------------|-----------------------------------------------------------------------------|
| `-h`, `--help`    | Print basic usage information.                                              |
| `-t`, `--token`   | GitHub personal access token (required).                                    |
| `-o`, `--org_name`| GitHub organization name (default: `Kaggle`).                               |
| `-a`, `--attributes` | Comma-separated list of attributes to analyze (default: all attributes). |
| `-c`, `--cloc`    | Count lines of code mode ON.                                                |
| `-l`, `--log`     | Print the clone log and save the repositories you cloned to local storage.  |


---

### **Default Settings**
- **Organization Name**: `Kaggle`
- **Attributes**: `commits`, `stars`, `contributors`, `branches`, `tags`, `forks`, `releases`, `closed_issues`, `environments`
- **Count lines of Code Mode**: OFF
- **Log and Save Repo Mode**: OFF

If you want to change the default settings, use the `-o`, `-a`, `-c` and `-l` options.

---

### **Examples**

1. **Get statistics for the default organization (`Kaggle`) with all attributes:**
   ```bash
   python get_statistics.py -t <GitHub token>
   ```
2. **Get statistics for a specific organization (`langchain-ai`) with selected attributes (`commits and stars`):**
   ```bash
   python get_statistics.py -t <GitHub token> -o langchain-ai -a commits,stars
   ```
3. **Get statistics for a specific organization (`langchain-ai`) with selected attributes (`commits, stars and languages:...`) and print the clone log in the terminal and save the repositories you cloned to local storage:**
   ```bash
   python get_statistics.py -t <GitHub token> -o langchain-ai -a commits,stars -c -l
   ```

---

## **Output**
The script generates a report with the following information:
- **Total and median values** for each attribute -> into a JSON file.

---

## **Requirements**
- Python 3.x
- `requests` library (install via `pip install requests`)
- GitHub personal access token (with `repo` scope): THIS IS Very Very Important!!!! The GitHub token is required to authenticate API requests and avoid rate limits. For how to get a personal access token in GitHub, please visit: [Tutorial](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)
- The `cloc` tool must be installed on your system for "Count lines of Code Mode" ON

---

## **Installation**
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/github-repo-stats.git
   cd github-repo-stats
   ```
2. Install the required dependencies (for Mac):
    ```bash
    pip install requests
    ```
    ```bash
    brew install cloc
    ```
3. Have fun and run the script:
    ```bash
    python get_statistics.py -t <GitHub token>
    ```

---

## **License**
I am lazy and don't have a lot of time left, I "promise" I will get a License later when needed. ^_^

---

## **Contributing**
Welcome to join me, even if it's a project for fun, please open an issue or submit a pull request for any improvements or bug fixes.

---

## **Contact**
For questions or feedback, please contact Like Wang at like.wang@mail.utoronto.ca.

---