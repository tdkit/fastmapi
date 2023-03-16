import sqlite3
conn = sqlite3.connect('data.db')
cursor = conn.cursor()

#conn.execute("""
# CREATE TABLE Napoje (
#     ID INTEGER PRIMARY KEY,
#     Name VARCHAR(255),
#     Ingredients TEXT
# );
# """)

cursor.execute(f"INSERT INTO Napoje (NAME, INGREDIENTS) \
        VALUES (?,?)", ('Kola', 'Tomato, Cheese'))
conn.commit()


cursor.execute('''SELECT * FROM Napoje''')
data = cursor.fetchall()
print(data)

conn.close()