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

        # Copy data to compute similarity score
        df = data.copy()
        df["score"] = 0

        # Add points for matches
        df.loc[df["State"] == state, "score"] += 2
        df.loc[df["Budget"] == budget, "score"] += 1
        df.loc[df["Motivation"] == motivation, "score"] += 1
        df.loc[df["Group"] == group, "score"] += 1
        df.loc[df["Duration"] == duration, "score"] += 1

        # Pick the best match
        best = df.sort_values("score", ascending=False).iloc[0]

        if best["score"] == 0:
            result = "No similar place found. Try different options."
        else:
            result = best["Place"]

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
