import json
import sqlite3

conn = sqlite3.connect("rosterdb.sqlite")
cur = conn.cursor()
cur.executescript("""
DROP TABLE IF EXISTS User;
DROP TABLE IF EXISTS Member;
DROP TABLE IF EXISTS Course;
                
CREATE TABLE User(
        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        name TEXT UNIQUE    
);

CREATE TABLE Course (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
                title TEXT UNIQUE
                
);
                
CREATE TABLE member (
                user_id INTEGER,
                course_id INTEGER,
                role INTEGER,  
                PRIMARY KEY(course_id,user_id)              
            
);

""")
fname = open(r"C:\Users\hesha\Downloads\roster_data.json").read()
json_data = json.loads(fname)
for line in json_data:
    name = line[0]
    title = line[1]
    # print(name,title)
    cur.execute("INSERT OR IGNORE INTO User (name) VALUES (?)", (name,))
    cur.execute("SELECT id FROM User WHERE name=?", (name,))
    user_id = cur.fetchone()[0]
    cur.execute("INSERT OR IGNORE INTO Course (title) VALUES (?)", (title,))
    cur.execute("SELECT id FROM Course WHERE title=?", (title,))
    course_id = cur.fetchone()[0]
    cur.execute(
        "INSERT OR REPLACE INTO member (user_id,course_id,role) VALUES (?,?,0)",
        (user_id, course_id),
    )
conn.commit()
import os

print(os.getcwd())
