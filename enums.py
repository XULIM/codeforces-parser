from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def list_values(cls):
        return list(map(lambda c: c.value, cls))


class cf_problem_field(ExtendedEnum):
    """
    Represents the the fields of a problem object from CodeForces.
    """

    CONTEST_ID = "contestId"
    PROBLEMSET_NAME = "problemsetName"
    ID = "index"
    NAME = "name"
    TYPE = "type"
    PTS = "points"
    RATING = "rating"
    TAGS = "tags"


class tables(ExtendedEnum):
    """
    Represents the tables created by the database.
    """

    PROBLEMS = "problems"
    CONTEST = "contest"


class methods(ExtendedEnum):
    """
    Represents the available URL methods when parsing the CodeForces API.
    """

    PROBLEM_SET = "problemset.problems?"
    PROBLEM_SET_STATUS = "problemset.recentStatus?"


class class_parameter(ExtendedEnum):
    """
    Represents the available URL parameters when parsing the CodeForces API.
    """

    TAGS = "tags"
    NAME = "problemsetName"
