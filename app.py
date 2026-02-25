from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

# Load the dataset once
data = pd.read_csv("tourism.csv")

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        state = request.form["state"]
        budget = request.form["budget"]
        duration = int(request.form["duration"])
        motivation = request.form["motivation"]
        group = request.form["group"]

        # Filter rows that match the user input
        filtered = data[
            (data["State"] == state) &
            (data["Budget"] == budget) &
            (data["Duration"] == duration) &
            (data["Motivation"] == motivation) &
            (data["Group"] == group)
        ]

        if not filtered.empty:
            # Take the first matching place
            result = filtered.iloc[0]["Place"]
        else:
            result = "No matching place found. Try different options."

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
