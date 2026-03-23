from flask import Flask, render_template, request
import pickle
import re

app = Flask(__name__)

# ===============================
# LOAD TRAINED MODEL + VECTORIZER
# ===============================
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

print("Training model...")

df = pd.read_csv("small_phishing_email.csv")

X = df["text_combined"].astype(str)
y = df["label"]

TfidfVectorizer(max_features=500, stop_words="english")
X_tfidf = vectorizer.fit_transform(X)

LogisticRegression(max_iter=100)
model.fit(X_tfidf, y)

print("Model trained successfully")
# ===============================
# SAME CLEANING FUNCTION
# ===============================
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


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
