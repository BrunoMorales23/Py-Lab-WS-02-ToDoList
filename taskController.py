import sqlite3 as sql
from sqlite3 import OperationalError

def createDB():
    connection = sql.connect("task_data.db")
    connection.commit()
    connection.close()

def createTable():
    connection = sql.connect("task_data.db")
    cursor = connection.cursor()
    try:
        cursor.execute(
            """CREATE TABLE tasks (
                name text,
                desc text,
                prio integer,
                date text,
                status integer
            )"""
        )
    except OperationalError:
        print("Table 'tasks' already exists")
        pass
    try:
        cursor.execute(
            """CREATE TABLE closedtasks (
                name text,
                desc text,
                prio integer,
                date text,
                status integer
            )"""
        )
    except OperationalError:
        print("Table 'closedtasks' already exists")
        pass
    try:
        cursor.execute(
            """CREATE TABLE deletedtasks (
                name text,
                desc text,
                prio integer,
                date text,
                status integer
            )"""
        )
    except OperationalError:
        print("Table 'deletedtasks' already exists")
        pass
    connection.commit()
    connection.close()

def insertRow(name,desc,prio,date,status):
    connection = sql.connect("task_data.db")
    cursor = connection.cursor()
    instruction = f"INSERT INTO tasks values ('{name}','{desc}','{prio}','{date}',{status})"
    cursor.execute(instruction)
    connection.commit()
    connection.close()

def getCurrentRows():
    connection = sql.connect("task_data.db")
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM tasks;")
    row_count = cursor.fetchone()[0]
    return row_count

def getAllData(table):
    connection = sql.connect("task_data.db")
    connection.row_factory = sql.Row
    cursor = connection.cursor()
    instruction = f"SELECT * FROM '{table}'"
    cursor.execute(instruction)
    data = cursor.fetchall()
    connection.commit()
    connection.close()
    return data

def pushDataIntoTable(name, input_table, output_table):
    connection = sql.connect("task_data.db")
    connection.row_factory = sql.Row
    cursor = connection.cursor()
    instruction = f"SELECT * FROM '{input_table}' WHERE name='{name}'"
    cursor.execute(instruction)
    data = cursor.fetchall()
    for row in data:
        cursor.execute(f"""
            INSERT INTO '{output_table}' (name, desc, prio, date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (row["name"], row["desc"], row["prio"], row["date"], row["status"]))
    instruction = f"DELETE FROM {input_table} WHERE name='{name}'"
    cursor.execute(instruction)
    connection.commit()
    connection.close()


def deleteRow(name, table):
    connection = sql.connect("task_data.db")
    cursor = connection.cursor()
    instruction = f"DELETE FROM '{table}' WHERE name='{name}'"
    cursor.execute(instruction)
    connection.commit()
    connection.close()

def cleanTable():
    connection = sql.connect("task_data.db")
    cursor = connection.cursor()
    instruction = f"DROP TABLE IF EXISTS tasks;"
    cursor.execute(instruction)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    createDB()
    createTable()
    cleanTable()