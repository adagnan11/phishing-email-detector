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


## 🏗️ System Architecture

The system follows a pipeline for processing and analyzing email content:

User Input → Text Cleaning → TF-IDF Vectorization → Machine Learning Model → Risk Scoring → Output + Explanation

- User Input: Email text entered by the user  
- Text Cleaning: Removes noise and normalizes text  
- TF-IDF: Converts text into numerical features  
- ML Model: Logistic Regression classifies the email  
- Risk Scoring: Combines model output with rule-based features  
- Output: Displays prediction, confidence, and explanation

## 🚀 How to Run Locally

1. Clone the repository:

2. Navigate to the project folder:
   cd phishing email-detector
3. Install dependencies:
pip install-r requirement.txt
   
4. Run the application:
   python app.py  

6. Open your browser and go to:
   http://localhost:1000

## 🌐 Live Demo
https://your-render-link
   
## ⚠️ Limitations

- The model relies mainly on text-based features and does not analyze email metadata such as sender address or headers  
- It may not detect highly sophisticated phishing attacks that mimic legitimate communication very closely  
- The dataset size is limited, which may affect generalization to unseen data  
- The system does not currently learn or update itself in real time

 ## 🔮 Future Improvements

- Integrate deep learning models such as LSTM or BERT for improved accuracy  
- Analyze email metadata (sender reputation, domain, headers)  
- Expand the dataset to include more diverse phishing examples  
- Add user authentication and history tracking  
- Deploy as a mobile-friendly or full-scale production application

- This project can be extended into a more robust cybersecurity tool with additional data sources and advanced models. 
       


