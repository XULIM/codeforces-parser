from database import parser_database
import os.path


def test_db_exists():
    db = parser_database()
    assert os.path.isfile("../results.db")


def test_problems_table_exists():
    db = parser_database()
    assert db.cursor.execute(
        """
        SELECT name FROM sqlite_master 
        WHERE type = "table" 
        AND name = "problems";
    """
    )


def test_problems_data_populated():
    db = parser_database()
    assert db.cursor.execute(
        """
        SELECT * FROM problems;
    """
    )
