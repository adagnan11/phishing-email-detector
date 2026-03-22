import pandas as pd
import re

from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# ===============================
# 1. LOAD DATA
# ===============================
print("Loading dataset...")

df = pd.read_csv(
    "phishing_email.csv",
    encoding="latin1",
    engine="python",
    on_bad_lines="skip"
)

print("Dataset loaded successfully")
print(df.shape)
print(df.columns)

# ===============================
# 2. CLEAN DATA
# ===============================
df.dropna(inplace=True)
df["text_combined"] = df["text_combined"].astype(str)

def clean_text(text):
    text = text.lower()
    text = re.sub(r"http\S+|www\S+", " ", text)
    text = re.sub(r"<.*?>", " ", text)
    text = re.sub(r"[^a-z\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

df["clean_text"] = df["text_combined"].apply(clean_text)

print("Text cleaned")
print(df[["text_combined", "clean_text"]].head(2))

print("Label distribution:")
print(df["label"].value_counts())
print("Label type:", df["label"].dtype)

# ===============================
# 3. SPLIT DATA
# ===============================
X = df["clean_text"]
y = df["label"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

# ===============================
# 4. VECTORIZE TEXT
# ===============================
tfidf = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)

X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# ===============================
# 5. TRAIN MODEL  ← THIS WAS MISSING
# ===============================
model = LogisticRegression(max_iter=1000)
model.fit(X_train_tfidf, y_train)

print("Model trained")

# ===============================
# 6. ERROR ANALYSIS
# ===============================
from sklearn.metrics import classification_report

# CREATE y_probs FIRST
y_probs = model.predict_proba(X_test_tfidf)[:, 1]
print("y_probs created:", len(y_probs))

# Threshold tuning
for t in [0.5, 0.4, 0.35, 0.3]:
    y_pred_t = (y_probs >= t).astype(int)
    print(f"\nThreshold = {t}")
    print(classification_report(y_test, y_pred_t))

# Default threshold analysis
THRESHOLD = 0.4
y_pred = (y_probs >= THRESHOLD).astype(int)


results = pd.DataFrame({
    "text": X_test.values,
    "true_label": y_test.values,
    "pred_label": y_pred,
    "phishing_prob": y_probs
})

false_negatives = results[
    (results["true_label"] == 1) &
    (results["pred_label"] == 0)
]

print("Number of false negatives:", len(false_negatives))
print(false_negatives.head(10)[["text", "phishing_prob"]])

false_negatives.to_csv("false_negatives.csv", index=False)
print("false_negatives.csv saved")
# False positives: legit emails predicted as phishing
false_positives = results[
    (results["true_label"] == 0) &
    (results["pred_label"] == 1)
]

print("Number of false positives:", len(false_positives))

# Save for analysis
false_positives.to_csv("false_positives.csv", index=False)
print("false_positives.csv saved")

from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

models = {
    "Logistic Regression": LogisticRegression(max_iter=1000),
    "Naive Bayes": MultinomialNB(),
    "Linear SVM": LinearSVC(),
    "Random Forest": RandomForestClassifier(n_estimators=100, random_state=42)
}

results = []

for name, model in models.items():
    print(f"\nTraining {name}...")
    model.fit(X_train_tfidf, y_train)
    y_pred = model.predict(X_test_tfidf)
    
    report = classification_report(y_test, y_pred, output_dict=True)
    
    results.append({
        "Model": name,
        "Accuracy": report["accuracy"],
        "Phishing Precision": report["1"]["precision"],
        "Phishing Recall": report["1"]["recall"],
        "Phishing F1": report["1"]["f1-score"]
    })

results_df = pd.DataFrame(results)

print("\nModel Comparison:")
print(results_df.sort_values(by="Phishing F1", ascending=False))

# ===============================
# SAVE LOGISTIC REGRESSION MODEL
# ===============================

import pickle

best_model = model   # <-- your trained logistic regression
vectorizer = tfidf   # <-- your TF-IDF vectorizer

with open("model.pkl", "wb") as f:
    pickle.dump(best_model, f)

with open("vectorizer.pkl", "wb") as f:
    pickle.dump(vectorizer, f)

print("Model and vectorizer saved successfully.")
import matplotlib.pyplot as plt
import os

# Create static folder if it doesn't exist
if not os.path.exists("static"):
    os.makedirs("static")

# Plot model performance
results_df.set_index("Model")[[
    "Phishing Precision",
    "Phishing Recall",
    "Phishing F1"
]].plot(kind="bar")

plt.title("Model Performance Comparison")
plt.ylabel("Score")
plt.xticks(rotation=45)
plt.tight_layout()

# Save image
plt.savefig("static/model_comparison.png")
plt.close()

print("Graph saved to static/model_comparison.png")
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Generate predictions (use default threshold 0.5 here)
y_pred = model.predict(X_test_tfidf)

# Create confusion matrix
cm = confusion_matrix(y_test, y_pred)

# Plot it
disp = ConfusionMatrixDisplay(confusion_matrix=cm)
disp.plot()

plt.title("Confusion Matrix")

# Save it
plt.savefig("static/confusion_matrix.png")
plt.close()

print("Confusion matrix saved!")