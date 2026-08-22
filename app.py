from flask import Flask, render_template, request, redirect, url_for, session
from rules import CATEGORIES, DIAGNOSTIC_TREES, DIAGNOSES
import os

app = Flask(__name__)
app.secret_key = "pc_expert_secret_key_change_in_production"

# Demo credentials
DEMO_USER = {
    "email": "student@unipart.edu.ng",
    "password": "password123",
    "name": "Olaniyan Al-azeem"
}

@app.route("/")
def index():
    if "page" not in session:
        session["page"] = "Home"
    if "selected_category" not in session:
        session["selected_category"] = None
    if "current_node" not in session:
        session["current_node"] = None
    if "diagnosis_result" not in session:
        session["diagnosis_result"] = None
    if "history" not in session:
        session["history"] = []

    current_question = None
    current_diagnosis = None
    category_label = ""

    if session.get("selected_category"):
        for cat in CATEGORIES:
            if cat["id"] == session["selected_category"]:
                category_label = cat["label"]
                break

    if session.get("selected_category") and session.get("current_node"):
        tree = DIAGNOSTIC_TREES.get(session["selected_category"], {})
        nodes = tree.get("nodes", {})
        current_question = nodes.get(session["current_node"])

    if session.get("diagnosis_result"):
        current_diagnosis = DIAGNOSES.get(session["diagnosis_result"])

    return render_template(
        "index.html",
        categories=CATEGORIES,
        page=session.get("page"),
        selected_category=session.get("selected_category"),
        category_label=category_label,
        current_question=current_question,
        current_diagnosis=current_diagnosis,
        step_number=len(session.get("history", [])) + 1,
        user=session.get("user"),
        login_error=session.pop("login_error", None)
    )

@app.route("/login", methods=["POST"])
def login():
    email = request.form.get("email")
    password = request.form.get("password")

    if email == DEMO_USER["email"] and password == DEMO_USER["password"]:
        session["user"] = DEMO_USER["name"]
        session["page"] = "Diagnose"
    else:
        session["login_error"] = "Invalid email or password. Use demo details below."
        session["page"] = "SignIn"

    return redirect(url_for("index"))

@app.route("/logout")
def logout():
    session.pop("user", None)
    session["page"] = "Home"
    return redirect(url_for("index"))

@app.route("/nav/<page_name>")
def navigate(page_name):
    session["page"] = page_name
    return redirect(url_for("index"))

@app.route("/select_category/<cat_id>")
def select_category(cat_id):
    session["selected_category"] = cat_id
    if cat_id in DIAGNOSTIC_TREES:
        session["current_node"] = DIAGNOSTIC_TREES[cat_id]["start_node"]
    else:
        session["diagnosis_result"] = "diag_psu_failure"
    return redirect(url_for("index"))

@app.route("/answer/<choice>")
def answer_question(choice):
    cat_id = session.get("selected_category")
    node_id = session.get("current_node")

    if cat_id and node_id:
        tree = DIAGNOSTIC_TREES.get(cat_id, {})
        nodes = tree.get("nodes", {})
        node = nodes.get(node_id)

        if node:
            history = session.get("history", [])
            history.append(node_id)
            session["history"] = history

            next_step = node.get(choice)
            if next_step in DIAGNOSES:
                session["diagnosis_result"] = next_step
                session["current_node"] = None
            else:
                session["current_node"] = next_step

    return redirect(url_for("index"))

@app.route("/back")
def go_back():
    history = session.get("history", [])
    if history:
        session["current_node"] = history.pop()
        session["history"] = history
    else:
        session["selected_category"] = None
        session["current_node"] = None
    return redirect(url_for("index"))

@app.route("/reset")
def reset_diagnosis():
    session["selected_category"] = None
    session["current_node"] = None
    session["diagnosis_result"] = None
    session["history"] = []
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)