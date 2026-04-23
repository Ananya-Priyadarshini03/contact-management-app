from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# ---------------- DATABASE ----------------
def get_db():
    conn = sqlite3.connect("contacts.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            address TEXT,
            email TEXT UNIQUE,
            phone TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

# ---------------- READ ----------------
@app.route("/")
def index():
    conn = get_db()
    contacts = conn.execute("SELECT * FROM contacts").fetchall()
    conn.close()
    return render_template("index.html", contacts=contacts)

# ---------------- CREATE ----------------
@app.route("/add", methods=["POST"])
def add():
    data = (
        request.form["first_name"],
        request.form["last_name"],
        request.form["address"],
        request.form["email"],
        request.form["phone"]
    )

    conn = get_db()
    try:
        conn.execute("""
            INSERT INTO contacts(first_name, last_name, address, email, phone)
            VALUES (?, ?, ?, ?, ?)
        """, data)
        conn.commit()
    except:
        print("Duplicate email error")
    conn.close()
    return redirect("/")

# ---------------- DELETE ----------------
@app.route("/delete/<int:id>")
def delete(id):
    conn = get_db()
    conn.execute("DELETE FROM contacts WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

# ---------------- UPDATE ----------------
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = get_db()

    if request.method == "POST":
        data = (
            request.form["first_name"],
            request.form["last_name"],
            request.form["address"],
            request.form["email"],
            request.form["phone"],
            id
        )
        conn.execute("""
            UPDATE contacts
            SET first_name=?, last_name=?, address=?, email=?, phone=?
            WHERE id=?
        """, data)
        conn.commit()
        conn.close()
        return redirect("/")

    contact = conn.execute("SELECT * FROM contacts WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("edit.html", contact=contact)

# ---------------- RUN ----------------
if __name__ == "__main__":
    app.run(debug=True)