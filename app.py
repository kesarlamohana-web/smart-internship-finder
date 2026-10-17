from flask import Flask, render_template, request, redirect, session, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "change-this-secret-key"

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def home():
    return redirect(url_for('login'))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        password = generate_password_hash(request.form["password"])
        branch = request.form["branch"]

        conn = get_db()
        try:
            conn.execute(
                "INSERT INTO students (name, email, password, branch) VALUES (?, ?, ?, ?)",
                (name, email, password, branch)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            conn.close()
            return render_template("register.html", error="Email already registered")
        conn.close()
        return redirect(url_for('login'))

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        conn = get_db()
        student = conn.execute("SELECT * FROM students WHERE email = ?", (email,)).fetchone()
        conn.close()

        if student and check_password_hash(student["password"], password):
            session["student_id"] = student["id"]
            session["student_name"] = student["name"]
            return redirect(url_for('profile'))
        else:
            return render_template("login.html", error="Invalid email or password")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/profile", methods=["GET", "POST"])
def profile():
    if "student_id" not in session:
        return redirect(url_for('login'))

    conn = get_db()
    saved = False
    if request.method == "POST":
        skills = request.form["skills"]
        location = request.form["location"]
        conn.execute(
            "UPDATE students SET skills = ?, location = ? WHERE id = ?",
            (skills, location, session["student_id"])
        )
        conn.commit()
        saved = True

    student = conn.execute("SELECT * FROM students WHERE id = ?", (session["student_id"],)).fetchone()
    conn.close()
    return render_template("profile.html", student=student, saved=saved)

@app.route("/internships")
def internship_list():
    if "student_id" not in session:
        return redirect(url_for('login'))

    location = request.args.get("location", "").strip()
    conn = get_db()
    if location:
        rows = conn.execute(
            "SELECT * FROM internships WHERE location LIKE ?",
            ("%" + location + "%",)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM internships").fetchall()
    conn.close()
    return render_template("internships.html", internships=rows, location=location)

@app.route("/recommendations")
def recommendations():
    if "student_id" not in session:
        return redirect(url_for('login'))

    conn = get_db()
    student = conn.execute("SELECT * FROM students WHERE id = ?", (session["student_id"],)).fetchone()
    rows = conn.execute("SELECT * FROM internships").fetchall()
    conn.close()

    my_skills = set(s.strip().lower() for s in (student["skills"] or "").split(",") if s.strip())

    results = []
    for item in rows:
        required = [s.strip() for s in (item["required_skills"] or "").split(",") if s.strip()]
        if not required:
            continue
        matched = [s for s in required if s.lower() in my_skills]
        missing = [s for s in required if s.lower() not in my_skills]
        percent = round(len(matched) / len(required) * 100)
        results.append({
            "internship": item,
            "percent": percent,
            "matched": matched,
            "missing": missing
        })

    results.sort(key=lambda r: r["percent"], reverse=True)
    return render_template("recommendations.html", results=results, student=student)

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "student_id" not in session:
        return redirect(url_for('login'))

    message = None
    conn = get_db()
    if request.method == "POST":
        conn.execute(
            "INSERT INTO internships (title, company, required_skills, location, duration, stipend, deadline, apply_link) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                request.form["title"],
                request.form["company"],
                request.form["required_skills"],
                request.form["location"],
                request.form["duration"],
                request.form["stipend"],
                request.form["deadline"],
                request.form["apply_link"],
            )
        )
        conn.commit()
        message = "Internship added successfully!"

    rows = conn.execute("SELECT * FROM internships ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("admin.html", internships=rows, message=message)

if __name__ == "__main__":
    app.run(debug=True)
