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
        """ """
        self.contest_id: int = problem["contestId"]
        self.index: str = problem["index"]
        self.name: str = problem["name"]
        self.rating: int = problem.get("rating", 0)
        self.tags: list[str] = problem.get("tags", [])
        self.solved_count = stats.get("solvedCount", 0)

    def __repr__(self):
        return ("objects.entry(\n\t"
                f"contest_id = {self.contest_id}\n\t"
                f"index = {self.index}\n\t"
                f"name = {self.name}\n\t"
                f"rating = {self.rating}\n\t"
                f"tags = [{"".join((e + "," for e in self.tags))}]\n\t"
                f"solved_count = {self.solved_count}"
                ")")

    def __str__(self):
        return (f"contest_id = {self.contest_id}\n"
                f"index = {self.index}\n"
                f"name = {self.name}\n"
                f"rating = {self.rating}\n"
                f"tags = '[{"".join((e + "," for e in self.tags))}]'\n"
                f"solved_count = {self.solved_count}")

    def conform_str(self):
        return (f"contestId={self.contest_id},"
                f"problemIndex={self.index},"
                f"name={self.name},"
                f"rating={self.rating},"
                f"tags='[{"".join((e + "," for e in self.tags))}]',"
                f"solvedCount={self.solved_count}")

    def __conform__(self, protocol):
        if protocol is sqlite3.PrepareProtocol:
            return self.conform_str()


class entries:
    def __init__(self, jsn):
        pass
