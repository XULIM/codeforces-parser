import sqlite3


class entry:
    """
    Represents an entry object for database.
    contest_id: int
    index: str
    name: str
    rating: int
    tags: list[str]
    solved_count: int
    """

    def __init__(self, problem: dict, stats: dict):
        """
        contest_id (int): has to be parsed, throws error if it DNE.
        index (str): has to be parsed, throws error if it DNE.
        name (str): defaults to "" if DNE.
        rating (int): defaults to 0 if DNE.
        tags (list[str]): defaults to [] (empty list) if DNE.
        solved_count (int): defaults to 0 if DNE or mismatch in problem and stats.
        """
        self.contest_id: int = problem["contestId"]
        self.index: str = problem["index"]
        self.name: str = problem.get("name", "")
        self.rating: int = problem.get("rating", 0)
        self.tags: list[str] = problem.get("tags", [])
        self.solved_count: int = (
            stats.get("solvedCount", 0)
            if (self.contest_id == stats["contestId"] and self.index == stats["index"])
            else 0
        )

    def __repr__(self):
        return (
            "objects.entry(\n\t"
            f"contest_id = {self.contest_id}\n\t"
            f"index = {self.index}\n\t"
            f"name = {self.name}\n\t"
            f"rating = {self.rating}\n\t"
            f"tags = [{",".join(e for e in self.tags)}]\n\t"
            f"solved_count = {self.solved_count}"
            ")"
        )

    def __str__(self):
        return (
            f"contest_id = {self.contest_id}\n"
            f"index = {self.index}\n"
            f"name = {self.name}\n"
            f"rating = {self.rating}\n"
            f"tags = [{"".join((e + ", " for e in self.tags))}]\n"
            f"solved_count = {self.solved_count}"
        )

    def conform_str_insert(self):
        return (
            "("
            f'{self.contest_id},'
            f'"{self.index}",'
            f'"{self.name}",'
            f'{self.rating},'
            f'"{",".join(e for e in self.tags)}",'
            f"{self.solved_count}"
            ")"
        )

    def conform_str(self):
        return (
            f"contestId={self.contest_id},"
            f"problemIndex={self.index},"
            f"name={self.name},"
            f"rating={self.rating},"
            f"tags='[{"".join((e + "," for e in self.tags))}]',"
            f"solvedCount={self.solved_count}"
        )

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return self.conform_str()


class entries:
    def __init__(self, res: dict):
        self.entries: list[entry] = []
        if len(res["problems"]) != len(res["problemStatistics"]):
            print(
                "WARNING: the problems dictionary and the problemStatistics dictionary are not "
                "matching in value, a default value of 0 for solved_count will be used."
            )

        for i in range(len(res["problems"])):
            self.entries.append(entry(res["problems"][i], res["problemStatistics"][i]))

    def conform_str_insert(self):
        return ",".join(x.conform_str_insert() for x in self.entries)

    def __str__(self):
        return "".join(str(x) + "\n" for x in self.entries)
