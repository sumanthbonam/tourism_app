@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        state = request.form["state"]
        budget = request.form["budget"]
        duration = int(request.form["duration"])
        motivation = request.form["motivation"]
        group = request.form["group"]

        # Make a copy to calculate scores
        df = data.copy()

        # Start with 0 score
        df["score"] = 0

        # Add points for matches (you can adjust weights)
        df.loc[df["State"] == state, "score"] += 2
        df.loc[df["Budget"] == budget, "score"] += 1
        df.loc[df["Motivation"] == motivation, "score"] += 1
        df.loc[df["Group"] == group, "score"] += 1
        df.loc[df["Duration"] == duration, "score"] += 1

        # Pick the row with highest score
        best = df.sort_values("score", ascending=False).iloc[0]

        # If even best score is 0, no similarity at all
        if best["score"] == 0:
            result = "No similar place found. Try different options."
        else:
            result = best["Place"]

    return render_template("index.html", result=result)
