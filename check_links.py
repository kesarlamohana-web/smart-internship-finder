import sqlite3

conn = sqlite3.connect("database.db")
conn.row_factory = sqlite3.Row

rows = conn.execute(
    "SELECT id, title, company, apply_link FROM internships ORDER BY id"
).fetchall()

for row in rows:
    print(f"\nID: {row['id']}")
    print(f"Internship: {row['title']}")
    print(f"Company: {row['company']}")
    print(f"Apply link: {row['apply_link']}")
    print("-" * 40)

print("Total internships:", len(rows))
conn.close()