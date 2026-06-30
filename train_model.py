import pandas as pd
from sklearn.linear_model import LinearRegression
import joblib

# Dataset load
data = pd.read_csv("student_data.csv")

# Input
X = data[["Attendance", "StudyHours", "PreviousMarks"]]

# Output
y = data["FinalMarks"]

# Model
model = LinearRegression()

# Train
model.fit(X, y)

# Save model
joblib.dump(model, "model.pkl")

print("Model Trained Successfully")