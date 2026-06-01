from flask import Flask, request, jsonify, render_template
import pickle
import json
import os
import sqlite3
from textblob import TextBlob

app = Flask(__name__)

# Load model and vectorizer
with open("model.pkl", "rb") as model_file:
    model = pickle.load(model_file)

with open("vectorizer.pkl", "rb") as vec_file:
    vectorizer = pickle.load(vec_file)

# Home route
@app.route("/")
def home():
    return render_template("index.html")


# Admin dashboard route
@app.route("/dashboard")
def dashboard():

    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT id, ticket_text, category, priority
    FROM tickets
    ORDER BY id DESC
    """)

    tickets = cursor.fetchall()

    # Analytics
    total_tickets = len(tickets)

    high_count = sum(1 for t in tickets if t[3] == "High")
    medium_count = sum(1 for t in tickets if t[3] == "Medium")
    low_count = sum(1 for t in tickets if t[3] == "Low")

    conn.close()

    return render_template(
        "dashboard.html",
        tickets=tickets,
        total_tickets=total_tickets,
        high_count=high_count,
        medium_count=medium_count,
        low_count=low_count
    )

# Classify ticket route
@app.route("/classify", methods=["POST"])
def classify_ticket():

    data = request.json
    original_text = data["text"]

    # Auto-correct spelling
    ticket_text = str(TextBlob(original_text).correct())

    # Vectorize input
    text_vector = vectorizer.transform([ticket_text])

    # Predict category
    prediction = model.predict(text_vector)[0]

    # Priority detection

    critical_keywords = [
    "production stopped",
    "server down",
    "system outage",
    "network outage",
    "cannot work",
    "business down"
    ]

    high_priority_keywords = [
    "not working",
    "computer not working",
    "laptop not working",
    "internet down",
    "vpn issue",
    "printer not working",
    "harassment",
    "harassed",
    "urgent",
    "harassment",
    "emergency",
    "violence",
    "abuse",
    "harssed"
    ]

    medium_priority_keywords = [
    "slow",
    "password reset",
    "salary",
    "delay",
    "complaint",
    "issue"
    ]

    ticket_lower = ticket_text.lower()

    priority = "Low"

    # Critical priority
    for word in critical_keywords:
        if word in ticket_lower:
            priority = "Critical"

    # High priority
    for word in high_priority_keywords:
        if word in ticket_lower and priority != "Critical":
          priority = "High"

    # Medium priority
    for word in medium_priority_keywords:
        if word in ticket_lower and priority not in ["Critical", "High"]:
            priority = "Medium"

    # Final result
    result = {
        "ticket": ticket_text,
        "predicted_category": prediction,
        "priority": priority
    }
    

    # Save to SQLite database
    conn = sqlite3.connect("tickets.db")
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO tickets (ticket_text, category, priority)
    VALUES (?, ?, ?)
    """, (ticket_text, prediction, priority))

    conn.commit()
    conn.close()
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)