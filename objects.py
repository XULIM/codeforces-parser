class entry:
    '''
    Represents an entry object for database.
    contest_id: int
    index: str 
    name: str
    rating: int
    tags: list[str]
    solved_count: int
    '''
    def __init__(self, problem: dict, stats: dict):
        '''
        '''
        self.contest_id: int = problem["contestId"]
        self.index: str = problem["index"]
        self.name: str = problem["name"]
        self.rating: int = problem.get("rating", 0)
        self.tags: list[str] = problem.get("tags", [])
        self.solved_count = stats.get("solvedCount", 0)

    def __str__(self):
        st = f'''
            contest_id = {self.contest_id} --\n
            index = {self.index} --\n
            name = {self.name} --\n
            rating = {self.rating} --\n
            tags = {"".join((e + " " for e in self.tags))} --\n
            solved_count = {self.solved_count} --\n
            '''
        return st

class entries:
    def __init__(self, jsn):
        pass
