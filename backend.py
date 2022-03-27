from datetime import datetime
from datetime import timedelta
import sqlite3
import ipywidgets as widgets


def get_cursor(path_to_db:str):
    conn = sqlite3.connect(path_to_db)
    cursor = conn.cursor()
    return conn, cursor

def table_update(path_to_db:str,sql:str):
    conn, cursor = get_cursor(path_to_db)
    cursor.execute(sql)
    conn.commit()
    conn.close()

def insert_task(name:str,path_to_db:str):
    sql = f'''INSERT INTO TO_DO (name,created_at)
              VALUES ('{name}',CURRENT_TIMESTAMP)'''
    table_update(path_to_db,sql)

def delete_task(id:int,path_to_db:str):
    sql = f'''DELETE FROM TO_DO WHERE unique_id =={id}'''
    table_update(path_to_db,sql)

def update_status(id:int,path_to_db:str):
    sql = f'''UPDATE TO_DO SET status = NOT status, completed_at = CURRENT_TIMESTAMP
              WHERE unique_id =={id}''' 
    table_update(path_to_db,sql)


def select_by_day(data:datetime,path_to_db:str):
    date_l = data.strftime("%Y-%m-%d")
    date_r = (data + timedelta(days=1)).strftime("%Y-%m-%d")
    conn, cursor = get_cursor(path_to_db)
    sql = f'''SELECT * from TO_DO WHERE created_at >= '{date_l}' AND created_at <= '{date_r}' '''
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


def show_items(items):
    list_of_hboxes = list()
    for it in items:
        idx = it[0]
        task = it[1]
        creation_time = datetime.strptime(it[2], "%Y-%m-%d %H:%M:%S")
        status = bool(it[4])
        text = f"{'+' if status else ' '} \t {creation_time.strftime('%H:%M')} \t {task}"
        button = widgets.Button(description='Completed', disabled=not(status))
        print(text)


def select_unfinished_tasks(path_to_db:str):
    conn, cursor = get_cursor(path_to_db)
    sql = f'''SELECT * from TO_DO WHERE status == 0 '''
    cursor.execute(sql)
    result = cursor.fetchall()
    return result



    