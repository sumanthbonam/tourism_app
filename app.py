from flask import Flask, render_template, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# ----------------- LOAD AND ENCODE DATA -----------------

# Read CSV
data = pd.read_csv("tourism.csv")

# Create encoders dict
encoders = {}

# Encode ONLY categorical columns as strings
for col in data.columns:
    if col != "Duration":  # Duration is numeric in your CSV
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col].astype(str))
        encoders[col] = le

# Features and target
X = data.drop("Place", axis=1)
y = data["Place"]

# Train model
model = DecisionTreeClassifier()
model.fit(X, y)

# ----------------- FLASK ROUTE -----------------

@app.route("/", methods=["GET", "POST"])
def home():
    result = None

    if request.method == "POST":
        state = request.form["state"]
        budget = request.form["budget"]
        duration = int(request.form["duration"])
        motivation = request.form["motivation"]
        group = request.form["group"]

        # Create one-row DataFrame
        user_input = pd.DataFrame(
            [[state, budget, duration, motivation, group]],
            columns=["State", "Budget", "Duration", "Motivation", "Group"]
        )

        # Encode using SAME encoders
        for col in ["State", "Budget", "Motivation", "Group"]:
            user_input[col] = encoders[col].transform(user_input[col].astype(str))

        # Duration is already int, no encoding
        # Predict
        prediction = model.predict(user_input)

        # Decode place
        predicted_place = encoders["Place"].inverse_transform(prediction)
        result = predicted_place[0]

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
