import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

internships = [
    ("Web Developer Intern", "TechNova", "HTML,CSS,JavaScript", "Bangalore", "3 months", "10000", "2026-11-30", "https://example.com/1"),
    ("Data Analyst Intern", "DataWorks", "Python,SQL,Excel", "Remote", "2 months", "8000", "2026-11-15", "https://example.com/2"),
    ("Python Developer Intern", "CodeBase", "Python,Flask,SQL", "Hyderabad", "6 months", "15000", "2026-12-01", "https://example.com/3"),
    ("Frontend Intern", "PixelCraft", "HTML,CSS,JavaScript,React", "Remote", "3 months", "12000", "2026-11-20", "https://example.com/4"),
    ("Java Developer Intern", "JavaWorks", "Java,SQL", "Chennai", "4 months", "10000", "2026-12-10", "https://example.com/5"),
]

cursor.executemany(
    "INSERT INTO internships (title, company, required_skills, location, duration, stipend, deadline, apply_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
    internships
)

conn.commit()
conn.close()
print(f"Inserted {len(internships)} internships")