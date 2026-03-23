from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

# ===============================
# LOAD TRAINED MODEL + VECTORIZER
# ===============================
import pickle

with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# ===============================
# ROUTES
# ===============================
@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    probability = None
    flags = []

    if request.method == "POST":
        email_text = request.form["email"]

        cleaned = clean_text(email_text)
        vectorized = vectorizer.transform([cleaned])

        # SAFE prediction (works for multiple models)
        if hasattr(model, "predict_proba"):
            prob = model.predict_proba(vectorized)[0][1]
        else:
            prob = model.decision_function(vectorized)[0]

        probability = round(prob * 100, 2)

        # Risk levels
        if prob >= 0.7:
            prediction = "🚨 High Risk Phishing"
        elif prob >= 0.4:
            prediction = "⚠️ Suspicious Email"
        else:
            prediction = "✅ Legitimate Email"

        # Explainability (keywords)
        keywords = ["urgent", "click", "verify", "password", "account"]
        flags = [word for word in keywords if word in cleaned]

    return render_template(
        "index.html",
        prediction=prediction,
        probability=probability,
        flags=flags
    )
if __name__ == "__main__":
    import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
