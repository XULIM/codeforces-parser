import requests
import json
# from parse import parser
from parse1 import parser
from parse1 import methods, class_parameter
import exceptions
from parse1 import class_parameter, methods


def main():
    try:
        par = parser()
        contest_id = 1922
        contest_index = "A"
        tag = class_parameter.TAGS
        problems = par.parse_method(methods.PROBLEM_SET_STATUS.value)
        print(problems.keys())
    except Exception as e:
        print(type(e))
        print(e.args)


if __name__ == "__main__":
    main()
