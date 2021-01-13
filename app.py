import os
from datetime import datetime
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

def create_app():
    app = Flask(__name__)
    client = MongoClient(os.environ.get("MONGODB_URI"))
    app.db = client.devblog

    @app.route("/", methods=["GET", "POST"])
    def home():
        if request.method == "POST":
            entry_content = request.form.get("content")
            date = datetime.now()
            app.db.entries.insert({"content": entry_content, "date": date})

        entries = list(app.db.entries.find({}).sort("date", -1))
        print(entries)
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                entry["date"].strftime("%b %d")
            )
            for entry in entries
        ]

        return render_template("home.html", entries=entries_with_date)
    
    return app

