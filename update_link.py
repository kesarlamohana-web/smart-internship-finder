import sqlite3

conn = sqlite3.connect("database.db")

new_link = input("Paste the real internship application URL: ").strip()

if new_link.startswith("https://") or new_link.startswith("http://"):
    conn.execute(
        "UPDATE internships SET apply_link = ? WHERE id = ?",
        (new_link, 6)
    )
    conn.commit()
    print("Application link updated successfully!")
else:
    print("Please enter a valid URL beginning with http:// or https://")

conn.close()