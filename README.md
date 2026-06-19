# 🏥 Diabetes Prediction System

A machine learning-powered web application that predicts diabetes risk using advanced ML algorithms. Built with Flask and scikit-learn, deployed on Render for real-time predictions.

## 🌐 Live Application

**[Access the Application Here]( https://diabetes-prediction-pbjm.onrender.com )**

---

## 🎯 Features

- **User Authentication**: Secure login system with role-based access (admin, user, doctor)
- **Diabetes Risk Prediction**: ML model predicts diabetes probability with confidence scores
- **Risk Level Assessment**: Categorizes risk as Low, Medium, or High based on prediction probability
- **Health Recommendations**: 
  - Diet recommendations tailored to diabetes management
  - Exercise guides and wellness tips
  - BMI calculator for quick health metrics
- **User Dashboard**: Personalized interface displaying prediction history and health insights
- **Responsive Design**: Mobile-friendly interface built with HTML/CSS

---

## 🛠️ Tech Stack

- **Backend**: Flask 2.0+
- **Machine Learning**: scikit-learn, NumPy, Pandas
- **Frontend**: HTML5, CSS3, Jinja2 templates
- **Deployment**: Render (Gunicorn WSGI server)
- **Model**: Trained diabetes prediction classifier with data scaling


## 🚀 Quick Start

### Local Development

**Prerequisites**: Python 3.7+, pip, virtualenv

```powershell
# Clone or navigate to the project
cd ml_diabetes_prediction

# Create and activate virtual environment
python -m venv venv
venv\Scripts\Activate

# Install dependencies
pip install -r requirements.txt

# Run Flask development server
python app.py

# Access at http://localhost:5000
```


## 📁 Project Structure

```
ml_diabetes_prediction/
├── app.py                    # Flask application & routing
├── train_model.py           # Model training script
├── diabetes.csv             # Training dataset
├── diabetes_model.pkl       # Trained ML model
├── scaler.pkl               # Data preprocessing scaler
├── requirements.txt         # Python dependencies
├── Procfile                 # Render deployment config
├── static/
│   └── style.css           # Application styling
└── templates/              # HTML templates
    ├── index.html          # Home page
    ├── login.html          # Authentication page
    ├── result.html         # Prediction results
    ├── health_tips.html    # Wellness information
    ├── diet_recommendations.html
    ├── exercise_guide.html
    ├── bmi_calculator.html
    ├── risk_assessment.html
    └── about.html
```

---

## 🤖 ML Model Details

- **Algorithm**: Classification model (trained on medical data)
- **Features**: 8 health metrics (pregnancies, glucose, blood pressure, skin thickness, insulin, BMI, diabetes pedigree function, age)
- **Output**: Binary classification (Diabetic / Non-Diabetic) with probability scores
- **Preprocessing**: Standardized scaling for optimal predictions

---

## 🔒 Security Notes

- Default credentials are for demo purposes only; change them in production
- `SECRET_KEY` is randomized on each deployment; set a strong value in environment variables
- HTTPS is enforced on Render
- Session-based authentication prevents unauthorized access

---

## 📊 Input Validation

The application validates all health metric inputs to ensure:
- Pregnancies ≥ 0
- Glucose, Blood Pressure, BMI, Age > 0
- All inputs are numerical values

Invalid inputs trigger helpful error messages with guidance.

---


## 🎓 Educational Value

This project demonstrates:
- End-to-end ML deployment (training → packaging → deployment)
- Flask web framework best practices
- User authentication and session management
- Production-ready Python application structure
- Cloud deployment with Render

---

## 📝 License

This project is open source and available for educational and research purposes.

---

## 📧 Support

For issues, feature requests, or contributions, feel free to open an issue or pull request on the GitHub repository.

---

