import sqlite3
conn = sqlite3.connect("documents.db")
cursor = conn.cursor()

def clearDB(cursor):
    cursor.execute("""DROP TABLE document;""")
def initDB(cursor):
    sql_command = """
    CREATE TABLE IF NOT EXISTS document (
    docID INTEGER PRIMARY KEY,
    source VARCHAR(30),
    content TEXT
    );
    """
    cursor.execute(sql_command)

def initTest(cursor):
    sql_command = """INSERT INTO document (docID, source, content)
    VALUES (NULL, "Twitter", "Testing");"""
    cursor.execute(sql_command)

def closeDB(save=True):
    global conn
    if save:
        conn.commit()
    conn.close()

def execute(command):
    global cursor
    cursor.execute(command)
    return cursor.fetchall()

if __name__ == "__main__":
    #initDB(cursor)
    #initTest(cursor)
    print(execute("SELECT * from document"))
    closeDB()