import sqlite3

class Database:
    def __init__(self, dbname):
        self.dbname = dbname
        self.db, self.cursor = self.make_cursor()

    def make_cursor(self):
        with sqlite3.connect(self.dbname) as db:
            cursor = db.cursor()
            return db, cursor

    def columns(self, db_columns):
        string = ""
        for nr, column in enumerate(db_columns):
            name, column_type = column
            if nr + 1 == len(db_columns):
                string += f"{name} {column_type}"
            else:
                string += f"{name} {column_type}, "
        return string

    def create(self, table_name, db_columns):
        try:
            self.cursor.execute(f"CREATE TABLE {table_name} (ID INTEGER PRIMARY KEY, {self.columns(db_columns)})")
        except sqlite3.OperationalError as E:
            print(E)

    def insert(self, table_name: str, data: tuple):
        row_names = ""
        amt_values = ""
        rows = self.cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
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
            try:
                self.cursor.execute(query, data)
                self.db.commit()
            except sqlite3.IntegrityError as E:
                print(E)
                print("something went wrong")

    def delete(self, table_name: str, row_id: int):
        self.cursor.execute(f"DELETE FROM {table_name} WHERE ID=?", (row_id,))
        self.db.commit()

    def select_all(self, table_name):
        self.cursor.execute(f"SELECT * FROM {table_name}")
        data = self.cursor.fetchall()
        return data
    
    def select_by_column(self, table_name, column, column_content):
        self.cursor.execute(f"SELECT * FROM {table_name} where {column}=?", (column_content, ))
        data = self.cursor.fetchall()
        return data

    def select_by_keyword(self, table_name, column, keyword):
        #self.cursor.execute("SELECT * FROM relics where COMMON LIKE ?", ("%odonata%", ))
        #self.cursor.execute("SELECT * FROM relics where UNCOMMON LIKE ?", ("%odonata%", ))
        #self.cursor.execute("SELECT * FROM relics where RARE LIKE ?", ("%odonata%", ))
        self.cursor.execute(f"SELECT * FROM {table_name} where {column} LIKE ?", (f"%{keyword}%", ))
        data = self.cursor.fetchall()
        return data

    def print_columns(self, table_name):
        columns = []
        data = self.cursor.execute(f"PRAGMA table_info({table_name})").fetchall()
        for i in data:
            name = i[1]
            column_type = i[2]
            columns.append(f"Name: {name} - Type: {column_type}")

        for column in columns:
            print(column)

    def print_tables(self):
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table'")
        print(self.cursor.fetchall())

    def drop(self, table_name):
        print(f"we are about to drop table: {table_name} like it's hot. There is no going back")
        input("")
        try:
            self.cursor.execute(f"DROP TABLE {table_name}")
        except sqlite3.OperationalError as E:
            print(E)


def main():
    print("for testing")

if __name__ == "__main__":
    main()
