import sqlite3

conn = sqlite3.connect("data.db")

with open("backup.sql", "w", encoding="utf-8") as f:
    for line in conn.iterdump():
        f.write(line + "\n")

conn.close()

print("Export completed!")