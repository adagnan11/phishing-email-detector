# phishing-email-detector
Machine learning-based phishing email detection system with a Flask web app, model evaluation, and visualization dashboard.
# 🔐 Phishing Email Detection System

## 📌 Overview
This project is a machine learning-based system designed to detect phishing emails. It analyzes the content of an email and classifies it as either phishing or legitimate.

In addition to classification, the system provides a confidence score and explains why an email may be suspicious. The goal is not only to improve detection accuracy but also to make the results understandable for users.

---

## 🚨 Problem Statement
Phishing attacks are one of the most common cybersecurity threats. Many users struggle to identify malicious emails, especially when they appear legitimate.

Traditional filtering systems often lack transparency, making it difficult for users to trust automated decisions. This project addresses that issue by combining machine learning with explainable outputs.

---

## 💡 Solution
This project implements a hybrid phishing detection system that combines:

- Machine Learning (Logistic Regression)
- Natural Language Processing (TF-IDF)
- Rule-based detection (keywords and suspicious links)

The system evaluates email content and enhances predictions using additional indicators such as URLs and common phishing terms.

---

## ⚙️ Features

- 🔍 Detects phishing vs legitimate emails
- 📊 Confidence score with visual risk bar
- 🧠 Explainable AI (human-readable reasons)
- 🌐 Web application using Flask
- ⚡ Real-time analysis

---

## 🧠 Technologies Used

- Python
- Flask
- Scikit-learn
- Pandas / NumPy
- HTML / CSS

---

## 🏗️ System Architecture
