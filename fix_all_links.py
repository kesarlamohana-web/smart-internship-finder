import sqlite3
from urllib.parse import quote

conn = sqlite3.connect("database.db")

searches = {
    1: "Web Developer Intern",
    2: "Data Analyst Intern",
    3: "Python Developer Intern",
    4: "Frontend Developer Intern",
    5: "Java Developer Intern",
}

for internship_id, keyword in searches.items():
    link = (
        "https://www.linkedin.com/jobs/search/"
        "?keywords=" + quote(keyword)
        + "&location=India"
    )
    conn.execute(
        "UPDATE internships SET apply_link = ? WHERE id = ?",
        (link, internship_id)
    )

conn.commit()
conn.close()

print("Five internship search links updated!")