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
    parser.get_problem(contestId, index)
