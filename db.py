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

def initDBs(cursor):
    sql_command = """
    CREATE TABLE IF NOT EXISTS RedditSubmission (
    docID VARCHAR(30) PRIMARY key,
    score INTEGER,
    author VARCHAR(30),
    golds INTEGER,
    url VARCHAR(100),
    subreddit VARCHAR(30),
    time TIMESTAMP,
    nsfw BOOLEAN,
    title VARCHAR(50),
    text TEXT
    );
    """
    cursor.execute(sql_command)

def insert_reddit_post(submission):
    execute("""
INSERT INTO RedditSubmission ( docID, score, author, golds, url, subreddit, time, nsfw, title, text) 
VALUES ({0}, {1}, {2}, {3}, {4}, {5}, {6}, {7}""".format(
    submission['id'],
    submission['score'],
    submission['author'],
    submission['golds'],
    submission['url'],
    submission['subreddit'],
    int(submission['time']), 
    1 if submission['nsfw'] else 0,
    submission['title'],
    submission['text']))
def generateID(id):
    return id
def closeDB(save=True):
    global conn
    if save:
        conn.commit()
    conn.close()
def commit():
    conn.commit()
def execute(command):
    global cursor
    cursor.execute(command)
    return cursor.fetchall()

if __name__ == "__main__":
    #initDB(cursor)
    initDBs(cursor)
    print(execute("SELECT * from document"))
    closeDB()
