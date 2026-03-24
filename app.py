from flask import Flask, render_template, request
import pickle
import re
import os
import zipfile

app = Flask(__name__)

# ==============================
# EXTRACT MODEL IF NEEDED
# ==============================

if not os.path.exists("model.pkl"):
    print("Extracting model.zip...")

    if os.path.exists("model.zip"):
        with zipfile.ZipFile("model.zip", "r") as zip_ref:
            zip_ref.extractall()
    else:
        print("ERROR: model.zip not found!")

# ==============================
# LOAD MODEL + VECTORIZER
# ==============================

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
    flags = None

    try:
        if request.method == "POST":
            email_text = request.form["email"]

            cleaned = clean_text(email_text)
            vectorized = vectorizer.transform([cleaned])

            prob = model.predict_proba(vectorized)[0][1]

            threshold = 0.4

            if prob >= threshold:
                prediction = "⚠️ Phishing Email"
            else:
                prediction = "✅ Legitimate Email"

            probability = round(prob * 100, 2)

        return render_template(
            "index.html",
            prediction=prediction,
            probability=probability,
            flags=flags
        )

    except Exception as e:
        return f"ERROR: {str(e)}"
