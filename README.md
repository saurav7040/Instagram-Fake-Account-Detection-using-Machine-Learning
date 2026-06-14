📸 Instagram Fake Account Detection using Machine Learning
📌 Project Description

This project is a Machine Learning-based system that detects whether an Instagram account is Fake or Real based on profile attributes such as followers, following, posts, bio, and external links.

The model learns patterns from labeled data and classifies accounts using algorithms like Random Forest / Logistic Regression / SVM.

This project is useful for:

Social media security analysis
Bot detection systems
Fake profile prevention
Data science portfolio project
🚀 Features
Detects fake Instagram accounts using ML
Data preprocessing and feature engineering
Model training and evaluation
Accuracy measurement and confusion matrix
Easy-to-use prediction system
Optional Streamlit web app integration
🧠 Machine Learning Workflow
Data Collection (Instagram profile dataset)
Data Cleaning & Preprocessing
Feature Selection
Train-Test Split
Model Training
Logistic Regression
Random Forest Classifier
Support Vector Machine (SVM)
Model Evaluation
Prediction (Fake / Real)
📊 Features Used
Number of posts
Number of followers
Number of following
Bio length
External URL presence
Profile picture availability
Account privacy status
🛠️ Tech Stack
Python 🐍
Pandas
NumPy
Scikit-learn
Matplotlib / Seaborn
Jupyter Notebook
📁 Project Structure
Instagram-Fake-Account-Detector/
│
├── dataset/
│   └── instagram.csv
│
├── model/
│   └── fake_account_model.pkl
│
├── notebook/
│   └── model_training.ipynb
│
├── app.py
├── requirements.txt
└── README.md
⚙️ Installation
git clone https://github.com/your-username/Instagram-Fake-Account-Detector.git
cd Instagram-Fake-Account-Detector
pip install -r requirements.txt
▶️ How to Run
1. Run Jupyter Notebook (Training)
jupyter notebook
2. Run Streamlit App (Optional)
streamlit run app.py
🤖 Model Accuracy
Model	Accuracy
Random Forest	~92%
Logistic Regression	~88%
SVM	~90%
📌 Output Example
Input: Instagram Profile Data
Output: Fake Account ❌ / Real Account ✅
📷 Use Cases
Detect fake influencers
Identify bot accounts
Improve social media security
Academic ML project
👨‍💻 Author

Saurav Gaikwad
BCA Graduate | MCA Student
Interested in Python, Machine Learning & AI Projects

📜 License

This project is licensed under the MIT License.

⭐ Future Improvements
Deep Learning model integration
Real-time Instagram API integration
Advanced bot behavior detection
Deploy on cloud (AWS / Streamlit Cloud)
