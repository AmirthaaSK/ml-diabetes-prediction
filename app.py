from flask import Flask, render_template, request, redirect, url_for, session
import pickle
import numpy as np
import os
from functools import wraps

print(os.getcwd())
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "diabetes_prediction_secret_key_2024")

# Load model and scaler (files expected in project root)
model_path = os.path.join(os.path.dirname(__file__), "diabetes_model.pkl")
scaler_path = os.path.join(os.path.dirname(__file__), "scaler.pkl")
model = pickle.load(open(model_path, "rb"))
scaler = pickle.load(open(scaler_path, "rb"))

# Sample user database (in production, use a real database)
users = {
    "admin": "admin123",
    "user": "user123",
    "doctor": "doctor123"
}

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route("/")
def index():
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        
        if username in users and users[username] == password:
            session['user'] = username
            return redirect(url_for('home'))
        else:
            return render_template("login.html", error="Invalid username or password")
    
    return render_template("login.html")

@app.route("/home")
@login_required
def home():
    return render_template("index.html", username=session.get('user'))

@app.route("/predict", methods=["POST"])
@login_required
def predict():
    try:
        pregnancies = float(request.form["pregnancies"])
        glucose = float(request.form["glucose"])
        bloodpressure = float(request.form["bloodpressure"])
        skinthickness = float(request.form["skinthickness"])
        insulin = float(request.form["insulin"])
        bmi = float(request.form["bmi"])
        dpf = float(request.form["dpf"])
        age = float(request.form["age"])

        # Validate inputs
        if not all([pregnancies >= 0, glucose > 0, bloodpressure > 0, age > 0, bmi > 0]):
            return render_template("index.html", error="Please enter valid positive values", username=session.get('user'))

        data = np.array([[pregnancies,
                          glucose,
                          bloodpressure,
                          skinthickness,
                          insulin,
                          bmi,
                          dpf,
                          age]])

        data = scaler.transform(data)

        prediction = model.predict(data)[0]
        probability = model.predict_proba(data)[0][1] * 100

        if prediction == 1:
            result = "Diabetic"
            risk_level = "High Risk" if probability > 70 else "Medium Risk" if probability > 40 else "Low Risk"
        else:
            result = "Non-Diabetic"
            risk_level = "Low Risk"

        return render_template(
            "result.html",
            prediction=result,
            probability=round(probability, 2),
            risk_level=risk_level,
            username=session.get('user'),
            pregnancies=pregnancies,
            glucose=glucose,
            bloodpressure=bloodpressure,
            age=age,
            bmi=bmi
        )
    except ValueError:
        return render_template("index.html", error="Please enter valid numerical values", username=session.get('user'))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route("/health-tips")
@login_required
def health_tips():
    return render_template("health_tips.html", username=session.get('user'))

@app.route("/diet-recommendations")
@login_required
def diet_recommendations():
    return render_template("diet_recommendations.html", username=session.get('user'))

@app.route("/exercise-guide")
@login_required
def exercise_guide():
    return render_template("exercise_guide.html", username=session.get('user'))

@app.route("/risk-assessment")
@login_required
def risk_assessment():
    return render_template("risk_assessment.html", username=session.get('user'))

@app.route("/about")
@login_required
def about():
    return render_template("about.html", username=session.get('user'))

@app.route("/bmi-calculator")
@login_required
def bmi_calculator():
    return render_template("bmi_calculator.html", username=session.get('user'))

if __name__ == "__main__":
    app.run(debug=True)