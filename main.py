import requests
import json
from parse import parser

if __name__ == "__main__":
    api_key = "https://codeforces.com/api/"
    problem_key = "problemset.problems"
    attr = ["problemSet.name", "tags"]
    tags = ["math", "implementation"]

    contestId = 1922
    index = "A"
    pp = parser()
    print(pp.get_all_problems())
    filtered_problems = pp.get_filtered_problems({"contestId": 1922})
    print((x for x in filtered_problems))
