import requests
import json

if __name__ == "__main__":
    api_key = "https://codeforces.com/api/"
    problem_key = "problemset.problems"
    attr = ["problemSet.name", "tags"]
    tags = ["math", "implementation"]

    response = requests.get(api_key + problem_key)

    problems = json.loads(response.json()["result"]["problems"])
