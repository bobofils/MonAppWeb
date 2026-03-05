from flask import Flask, render_template, request, redirect, send_file, Response
import sqlite3
import os
import pandas as pd
import csv

app = Flask(__name__)

# Création base de données
def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # table des tâches
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT NOT NULL
        )
    """)

    # table des utilisateurs
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    """)

    conn.commit()
    conn.close()
@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username,password) VALUES (?,?)",(username,password))
        conn.commit()
        conn.close()

        return redirect("/login")

    return render_template("register.html")
@app.route("/login", methods=["GET","POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE username=? AND password=?",(username,password))
        user = cursor.fetchone()

        conn.close()

        if user:
            return redirect("/")
        else:
            return "Utilisateur incorrect"

    return render_template("login.html")

@app.route("/")
def index():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()
    return render_template("index.html", tasks=tasks)

@app.route("/add", methods=["POST"])
def add():
    task = request.form.get("task")
    if task:
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO tasks (content) VALUES (?)", (task,))
        conn.commit()
        conn.close()
    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

# Export CSV
@app.route("/export")
def export_tasks():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks")
    tasks = cursor.fetchall()
    conn.close()

    def generate():
        yield "id,content\n"
        for task in tasks:
            yield f"{task[0]},{task[1]}\n"

    return Response(generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=tasks.csv"})

# Export Excel
@app.route("/export_excel")
def export_excel():
    conn = sqlite3.connect("database.db")
    df = pd.read_sql_query("SELECT * FROM tasks", conn)
    conn.close()

    file = "tasks.xlsx"
    df.to_excel(file, index=False)

    return send_file(file, as_attachment=True)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
@app.route("/stats")
def stats():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]

    conn.close()

    return render_template("stats.html", total=total)