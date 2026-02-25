from flask import Flask, render_template, request
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

# 1. Load data
data = pd.read_csv("tourism.csv")

# 2. Encode categorical columns
encoders = {}
for col in data.columns:
    if data[col].dtype == "object":
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col])
        encoders[col] = le

# 3. Split features and target
X = data.drop("Place", axis=1)
y = data["Place"]

# 4. Train model
model = DecisionTreeClassifier()
model.fit(X, y)

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        state = request.form["state"]
        budget = request.form["budget"]
        duration = int(request.form["duration"])
        motivation = request.form["motivation"]
        group = request.form["group"]

        # Create DataFrame from user input
        user_input = pd.DataFrame(
            [[state, budget, duration, motivation, group]],
            columns=["State", "Budget", "Duration", "Motivation", "Group"]
        )

        # Apply the same encoders to user input
        for col in user_input.columns:
            if col in encoders and user_input[col].dtype == "object":
                user_input[col] = encoders[col].transform(user_input[col])

        # Predict
        prediction = model.predict(user_input)

        # Decode predicted place
        predicted_place = encoders["Place"].inverse_transform(prediction)
        result = predicted_place[0]

    return render_template("index.html", result=result)

if __name__ == "__main__":
    app.run(debug=True)
