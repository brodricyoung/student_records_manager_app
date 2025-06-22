# Overview

This software is a command-line based Student Record Manager that tracks student progress across various competencies using a SQL relational database. It allows the user to add students and competencies, each to thier own table, and assign grades for specific competencies to students to its own table linked to the other two. The program also can generate individual student reports and delete records from the tables when necessary.

This project was built to establish a beginning understanding of SQLite relational databases. It also helped me practice the Python programming language and writing modular, maintainable code that handles real-world data relationships and provides useful feedback to users. My goal with this software was to create a functional system that mimics basic operations of a grade-tracking or competency-based learning management system.

[Software Demo Video](https://youtu.be/CGt_4dSUKdk)

# Relational Database

This application uses a SQLite relational database named student_records.db. The database structure includes three interrelated tables:
- students: Stores a unique student_id and name.

- competencies: Stores a unique competency_id and title.

- grades: Tracks which student earned which grade (1–4) on which competency, linking back to both the students and competencies tables using foreign keys.

Each student can have multiple grades (one per competency), and each competency can apply to multiple students, forming a many-to-many relationship via the grades table.

# Development Environment

Programming Language: Python 3
Database: SQLite3
Editor: Visual Studio Code
Libraries: sqlite3 (built-in Python library for SQLite interaction)

# Useful Websites

{Make a list of websites that you found helpful in this project}

- [TutorialsPoint: SQLite - Python](https://www.tutorialspoint.com/sqlite/sqlite_python.htm)
- [SQLite Tutorial](https://www.sqlitetutorial.net/)
- [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
- [SQL - W3Schools](https://www.w3schools.com/sql/)
- [Relational Databases - Oracle](https://www.oracle.com/database/what-is-a-relational-database/)
- [Relational Databases - Wikipedia](https://en.wikipedia.org/wiki/Relational_database)
- [ChatGPT](https://chatgpt.com/)

# Future Work

- Improve input validation and handle invalid formats more gracefully.
- Prevent duplicate entries more effectively with user feedback.
- Add the ability to update student names, competency titles, and grades.
- Display all students or all competencies in a list on demand.
- Implement search functionality by partial name or title.
- Convert the CLI interface to a GUI or web-based interface using Tkinter, Flask, or Django.
- Add export features to save reports as text or PDF files.
- Add import features to pull in batches of competencies or students.
- Store timestamps for when each grade was recorded or updated.
