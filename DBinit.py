import sqlite3
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

conn.execute("""
CREATE TABLE Pizza (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(255),
    Ingredients TEXT
);
""")

conn.execute("""
CREATE TABLE Napoje (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(255),
    Ingredients TEXT
);
""")

conn.execute("""
CREATE TABLE Deserty (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(255),
    Ingredients TEXT
);
""")

conn.execute("""
CREATE TABLE Cenik (
    ID INTEGER PRIMARY KEY,
    Name VARCHAR(255),
    Price INT
);
""")

conn.close()