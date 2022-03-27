import sqlite3
import random
import numpy as np
from datetime import datetime
from backend import get_cursor


def datetime_from_seconds(sec: int):
    return datetime.fromtimestamp(sec)


def create_table(path_to_db = "to_do.db"):
    conn, cursor = get_cursor(path_to_db)

    sql ='''CREATE TABLE TO_DO(
    unique_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name CHAR(255),
    created_at TIMESTAMP,
    completed_at TIMESTAMP,
    status bool DEFAULT False
    )'''
    with conn:
        cursor.execute(sql)
        print("Table created successfully!")


def add_item(
    name: str,
    created_at: datetime,
    completed_at: datetime,
    status: bool,
    path_to_db = "to_do.db",
):
    conn, cursor = get_cursor(path_to_db)
    with conn:
        cursor.execute(f"INSERT INTO TO_DO (name, created_at, completed_at, status) VALUES (?,?,?,?)",
                        (name,
                        created_at.strftime("%Y-%m-%d %H:%M:%S"), 
                        completed_at.strftime("%Y-%m-%d %H:%M:%S"), 
                        status))
        conn.commit()


def generate_random_name():
    verbs = ['create', 'make', 'do', 'submit', 'download', 'complete', 'finish', 'update', 'write']
    topics = ['math', 'physics', 'science', 'english', 'french', 'ukrainian']
    nouns = ['homework', 'assignment', 'movie', 'book', 'article', 'program', 'exam', 'essay', 'tutorial']
    locations = ['at home', 'in the lab', "in the office"]
    return f"{random.choice(verbs)} {random.choice(topics)} {random.choice(nouns)} {random.choice(locations)}"


def add_random_item(
    path_to_db = "to_do.db",
):
    conn, cursor = get_cursor(path_to_db)
    itemname = generate_random_name()
    start = 1647800000
    created_seconds = start + random.randint(0, 700000)
    duration = int(np.clip(np.random.normal(loc=10800, scale=3600), a_min=100, a_max=None))
    completed_seconds = created_seconds + duration
    add_item(
        name=itemname,
        created_at=datetime_from_seconds(created_seconds),
        completed_at=datetime_from_seconds(completed_seconds),
        status=True,
        path_to_db=path_to_db
        )
    # conn.close()


def print_all(path_to_db):
    conn, cursor = get_cursor(path_to_db)
    with conn:
        cursor.execute("SELECT * FROM TO_DO")
        res = cursor.fetchall()
        for it in res:
            print(it)


if __name__ == "__main__":
    table_name = 'tasks.db'
    create_table(table_name)
    for _ in range(20):
        add_random_item(table_name)
    print_all(table_name)