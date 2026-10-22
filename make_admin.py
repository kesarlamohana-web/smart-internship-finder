import sqlite3

email = "lakshmimohanakesarla@gmail.com"

conn = sqlite3.connect("database.db")

try:
    columns = conn.execute(
        "PRAGMA table_info(students)"
    ).fetchall()

    column_names = [column[1] for column in columns]

    if "role" not in column_names:
        print("ERROR: The role column is missing.")
    else:
        cursor = conn.execute(
            "UPDATE students SET role = 'admin' WHERE email = ?",
            (email,)
        )

        if cursor.rowcount == 1:
            conn.commit()
            print("SUCCESS: Your account is now an admin.")
        else:
            print("ERROR: No account found with that email.")

finally:
    conn.close()