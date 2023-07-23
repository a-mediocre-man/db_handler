import sqlite3
from pprint import pprint

def transaction(func):
    print("Hello from the decorator")
    def wrapper(self, *args, **kwargs):
        with sqlite3.connect(self.dbname) as conn:
            cursor = conn.cursor()
            result = func(self, cursor, *args, **kwargs)
            conn.commit()
            return result
    return wrapper

class Database:
    def __init__(self, dbname):
        self.dbname = dbname

    def __repr__(self):
        return f"Database({self.dbname})"

    def columns(self, db_columns):
        string = ""
        for nr, column in enumerate(db_columns):
            name, column_type = column
            if nr + 1 == len(db_columns):
                string += f"{name} {column_type}"
            else:
                string += f"{name} {column_type}, "
        return string

    @transaction
    def create(self, cursor, table_name, db_columns):
        try:
            cursor.execute(f"CREATE TABLE {table_name} (ID INTEGER PRIMARY KEY, {self.columns(db_columns)})")
        except sqlite3.OperationalError as E:
            print(E)

    @transaction
    def insert(self, cursor, table_name: str, data: tuple):
        row_names = ""
        amt_values = ""
        rows = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
        del rows[0]


        if len(data) != len(rows):
            print("missmatch")
        else:
            for nr, row in enumerate(rows):
                name = row[1]
                if nr + 1 == len(rows):
                    row_names += f"{name}"
                    amt_values += "?"
                else:
                    row_names += f"{name}, "
                    amt_values += "?, "

            query = f"INSERT INTO {table_name} ({row_names}) VALUES ({amt_values})"
            cursor.execute(query, data)

    @transaction
    def delete(self, table_name: str, row_id: int):
        cursor.execute(f"DELETE FROM {table_name} WHERE ID=?", (row_id,))

    @transaction
    def select_all(self, cursor, table_name):
        cursor.execute(f"SELECT * FROM {table_name}")
        data = cursor.fetchall()
        pprint(data)
        return data
    
    @transaction
    def select_by_column(self, cursor, table_name, column, column_content):
        cursor.execute(f"SELECT * FROM {table_name} where {column}=?", (column_content, ))
        data = cursor.fetchall()
        return data

    @transaction
    def select_by_keyword(self, cursor, table_name, column, keyword):
        cursor.execute(f"SELECT * FROM {table_name} where {column} LIKE ?", (f"%{keyword}%", ))
        data = cursor.fetchall()
        return data

    @transaction
    def update(self, cursor, table_name, row_id, column_name, new_content):
        print(table_name, row_id, column_name, new_content)
        cursor.execute(f"UPDATE {table_name} SET {column_name}=? WHERE ID=?", (new_content, row_id))

    @transaction
    def print_columns(self, cursor, table_name):
        columns = []
        data = cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
        for i in data:
            name = i[1]
            column_type = i[2]
            columns.append(f"Name: {name} - Type: {column_type}")

        for column in columns:
            print(column)

    @transaction
    def print_tables(self, cursor):
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
        print(cursor.fetchall())

    @transaction
    def drop(self, cursor, table_name):
        print(f"we are about to drop table: {table_name} like it's hot. There is no going back")
        input("")
        try:
            cursor.execute(f"DROP TABLE {table_name}")
        except sqlite3.OperationalError as E:
            print(E)


def main():
    print("for testing")

if __name__ == "__main__":
    main()
