# 🎓 Student Performance Predictor

A Machine Learning-based web application that predicts student academic performance using attendance, study hours, and previous marks. The project provides an interactive dashboard, analytics, student management, and report generation through a user-friendly Streamlit interface.

---

## 📌 Project Overview

Student Performance Predictor is designed to help teachers and educational institutions analyze student performance, identify at-risk students, and make data-driven decisions.

The application predicts students' final performance using Machine Learning and provides detailed analytics through an interactive dashboard.

---

## ✨ Features

### 🔐 Authentication
- Secure Login System
- Admin Access
- Logout Functionality

### 🤖 Student Performance Prediction
- Predict Final Marks
- Attendance Analysis
- Risk Prediction (Low / Medium / High)

### 📊 Dashboard & Analytics
- Total Students
- Low Risk Students
- Medium Risk Students
- High Risk Students
- Average Predicted Marks
- Top Performer
- Lowest Performer

### 📈 Data Visualization
- Risk Distribution Pie Chart
- Attendance Bar Chart
- Predicted Marks Chart
- Attendance vs Predicted Marks Scatter Plot

### 🗄 Database Management
- SQLite Database
- Store Student Records
- Search Student
- Update Student Details
- Prediction History

### 📂 Bulk Operations
- Bulk CSV Upload
- Multiple Student Prediction

### 📄 Reports
- Download Student Report (PDF)
- Download Prediction Report (CSV)

### 🎨 User Interface
- Professional Dashboard
- Dark Theme
- Sidebar Navigation
- Responsive Layout

---

# 🛠 Technologies Used

- Python
- Streamlit
- Scikit-learn
- Pandas
- NumPy
- SQLite
- Matplotlib
- ReportLab
- Joblib

---

# 📁 Project Structure

```
Student-Performance-Predictor
│
├── app.py
├── train_model.py
├── student_data.csv
├── students.db
├── model.pkl
├── history.csv
│
├── auth_view.py
├── dashboard_view.py
├── predict_view.py
├── database_view.py
├── search_view.py
├── update_view.py
├── delete_view.py
├── bulk_view.py
│
├── common.py
├── requirements.txt
└── README.md
```

---

# ⚙️ Installation

### Clone Repository

```bash
git clone https://github.com/Priyanshuverma07/Student-Performance-Predictor.git
```

Move to project folder

```bash
cd Student-Performance-Predictor
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the project

```bash
streamlit run app.py
```

---

# 📊 Machine Learning Workflow

```
Student Data
      │
      ▼
Data Preprocessing
      │
      ▼
Model Training
      │
      ▼
Prediction
      │
      ▼
Risk Analysis
      │
      ▼
Dashboard
      │
      ▼
PDF Report
```

---

# 📷 Screenshots

### Login Page

(Add Screenshot)

---

### Dashboard

(Add Screenshot)

---

### Prediction Page

(Add Screenshot)

---

### Analytics Dashboard

(Add Screenshot)

---

### PDF Report

(Add Screenshot)

---

# 🚀 Future Enhancements

- Email Report
- Export Database to Excel
- Cloud Deployment
- Student Profile Images
- Performance Recommendation System
- Advanced Machine Learning Models
- Multi-user Authentication

---

# 🎯 Learning Outcomes

Through this project I learned:

- Machine Learning Model Development
- Data Analysis using Pandas
- Data Visualization
- Streamlit Web Development
- SQLite Database Management
- PDF Report Generation
- CRUD Operations
- Git & GitHub
- Python Project Structure

---

# 👨‍💻 Developer

**Priyanshu Verma**

B.Tech CSE (Artificial Intelligence)

BBD University, Lucknow

---

## 📫 Connect with Me

**GitHub**

https://github.com/Priyanshuverma07

---

⭐ If you like this project, don't forget to Star this repository.
