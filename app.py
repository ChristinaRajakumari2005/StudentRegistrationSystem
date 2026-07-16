from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

DATABASE = "students.db"


def create_table():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            email TEXT,
            department TEXT
        )
    """)

    conn.commit()
    conn.close()


@app.route("/")
def home():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()

    conn.close()

    return render_template("index.html", students=students)


@app.route("/register", methods=["POST"])
def register():

    name = request.form["name"]
    email = request.form["email"]
    department = request.form["department"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO students(name,email,department) VALUES(?,?,?)",
        (name, email, department)
    )

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("DELETE FROM students WHERE id=?", (id,))

    conn.commit()
    conn.close()

    return redirect("/")


@app.route("/edit/<int:id>")
def edit(id):

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM students WHERE id=?", (id,))
    student = cursor.fetchone()

    conn.close()

    return render_template("edit.html", student=student)


@app.route("/update/<int:id>", methods=["POST"])
def update(id):

    name = request.form["name"]
    email = request.form["email"]
    department = request.form["department"]

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE students
        SET name=?, email=?, department=?
        WHERE id=?
        """,
        (name, email, department, id)
    )

    conn.commit()
    conn.close()

    return redirect("/")


if __name__ == "__main__":
    create_table()
    app.run(debug=True)