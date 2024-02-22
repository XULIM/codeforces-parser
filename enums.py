from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))


class cf_problem_field(ExtendedEnum):
    CONTEST_ID = "contestId"
    PROBLEMSET_NAME = "problemsetName"
    ID = "index"
    NAME = "name"
    TYPE = "type"
    PTS = "points"
    RATING = "rating"
    TAGS = "tags"


class tables(ExtendedEnum):
    PROBLEMS = "problems"


class methods(ExtendedEnum):
    PROBLEM_SET = "problemset.problems?"
    PROBLEM_SET_STATUS = "problemset.recentStatus?"


class class_parameter(ExtendedEnum):
    TAGS = "tags"
    NAME = "problemsetName"
