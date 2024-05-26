from objects import entry


def entry_initializable():
    fake_problem = {
        "contestId": 1,
        "index": "A",
        "name": "hello world",
        "type": "PROGRAMMING",
        "rating": 800,
        "tags": ["implementation", "math"],
    }
    fake_stats = {"contestId": 1, "index": "A", "solvedCount": 1500}
    en = entry(fake_problem, fake_stats)
    assert (
        en.contest_id == 1
        and en.index == "A"
        and en.name == "hello world"
        and en.rating == 800
        and en.tags == ["implementation", "math"]
        and en.solved_count == 1500
    )
