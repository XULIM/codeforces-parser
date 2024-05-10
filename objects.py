class entry:
    def __init__(self, jsn):
        self.contest_id = jsn["problems"]["contestId"]
        self.index = jsn["problems"]["index"]
        self.name = jsn["problems"]["name"]
        self.rating = jsn["problems"]["rating"]
        self.tags = "".join([e + ":" for e in jsn["problems"]["tags"]])
        self.solved_count = jsn["problemStatistics"]["solvedCount"]
