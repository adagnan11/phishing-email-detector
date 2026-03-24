from flask import Flask, render_template, request
import pickle
import re
import os

app = Flask(__name__)

# LOAD MODEL
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("vectorizer.pkl", "rb") as f:
    vectorizer = pickle.load(f)

# CLEAN TEXT
def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    probability = None
    flags = []

    try:
        if request.method == "POST":
            email_text = request.form["email"]

            cleaned = clean_text(email_text)
            vectorized = vectorizer.transform([cleaned])

            prob = model.predict_proba(vectorized)[0][1]

            # ===============================
            # SMART FEATURES
            # ===============================
            url_flag = ("http" in email_text.lower()) or ("www" in email_text.lower())

            urgent_words = ["urgent", "verify", "password", "account", "login", "bank"]
            keyword_hits = [word for word in urgent_words if word in cleaned]

            risk_score = prob

            if url_flag:
                risk_score += 0.2

            if len(keyword_hits) >= 2:
                risk_score += 0.2

            # ===============================
            # PREDICTION
            # ===============================
            if risk_score >= 0.7:
                prediction = "🚨 High Risk Phishing"
            elif risk_score >= 0.4:
                prediction = "⚠️ Suspicious Email"
            else:
                prediction = "✅ Legitimate Email"

            probability = round(prob * 100, 2)

            # ===============================
            # FLAGS (EXPLANATION)
            # ===============================
            if url_flag:
                flags.append("Contains suspicious link")

            for word in keyword_hits:
                flags.append(f"Contains keyword: '{word}'")

        return render_template(
            "index.html",
            prediction=prediction,
            probability=probability,
            flags=flags
        )

    except Exception as e:
        return f"ERROR: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
