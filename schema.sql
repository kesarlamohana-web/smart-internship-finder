CREATE TABLE students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    branch TEXT,
    skills TEXT,
    location TEXT
);

CREATE TABLE internships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    company TEXT NOT NULL,
    required_skills TEXT,
    location TEXT,
    duration TEXT,
    stipend TEXT,
    deadline TEXT,
    apply_link TEXT
);