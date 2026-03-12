-- Drop tables if they exist to ensure a clean slate on initialization.
DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS quiz_recommendations;
DROP TABLE IF EXISTS timelines;
DROP TABLE IF EXISTS scholarships;
DROP TABLE IF EXISTS feedback;
DROP TABLE IF EXISTS user_tokens;
DROP TABLE IF EXISTS courses;

-- Create the users table with all profile fields.
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TEXT NOT NULL,
    dob TEXT,
    education TEXT,
    passout_year TEXT,
    stream TEXT,
    address TEXT,
    phone TEXT,
    -- NEW FIELDS ADDED FOR A MORE COMPREHENSIVE PROFILE
    gender TEXT,
    current_class TEXT,
    academic_interests TEXT
);

-- Create the table for courses.
CREATE TABLE courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    pathway TEXT,
    sub_pathway TEXT,
    stream TEXT,
    title TEXT NOT NULL,
    description TEXT,
    career_paths TEXT,
    exams TEXT
);

-- Create the table for storing quiz results.
CREATE TABLE quiz_recommendations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    recommendations TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create the table for timeline events.
CREATE TABLE timelines (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    event_date TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create the table for scholarships.
CREATE TABLE scholarships (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    eligibility TEXT,
    deadline TEXT,
    link TEXT
);

-- Create the table for user feedback.
CREATE TABLE feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

-- Create the table for storing user authentication tokens.
CREATE TABLE user_tokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    token TEXT UNIQUE NOT NULL,
    expires_at TEXT NOT NULL,
    created_at TEXT NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

