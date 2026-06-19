from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import pickle
import numpy as np
import os
from functools import wraps
import json
from datetime import datetime

print(os.getcwd())
app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "diabetes_prediction_secret_key_2024")

# Load model and scaler (files expected in project root)
model_path = os.path.join(os.path.dirname(__file__), "diabetes_model.pkl")
scaler_path = os.path.join(os.path.dirname(__file__), "scaler.pkl")

try:
    model = pickle.load(open(model_path, "rb"))
    scaler = pickle.load(open(scaler_path, "rb"))
except FileNotFoundError:
    print("⚠️ Warning: Model or scaler file not found. Please ensure diabetes_model.pkl and scaler.pkl exist.")
    model = None
    scaler = None

# Users database file
USERS_FILE = os.path.join(os.path.dirname(__file__), "users.json")
PREDICTIONS_FILE = os.path.join(os.path.dirname(__file__), "predictions.json")

# Initialize with demo users
DEFAULT_USERS = {
    "demo_user": "abc123",
    "admin": "admin123",
    "user": "user123",
    "doctor": "doctor123"
}

def load_users():
    """Load users from JSON file"""
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading users: {e}")
            return DEFAULT_USERS.copy()
    return DEFAULT_USERS.copy()

def save_users(users_dict):
    """Save users to JSON file"""
    try:
        with open(USERS_FILE, 'w') as f:
            json.dump(users_dict, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving users: {e}")
        return False

def load_predictions(username):
    """Load predictions for a user"""
    try:
        if os.path.exists(PREDICTIONS_FILE):
            with open(PREDICTIONS_FILE, 'r') as f:
                all_predictions = json.load(f)
                return all_predictions.get(username, [])
    except Exception as e:
        print(f"Error loading predictions: {e}")
    return []

def save_prediction(username, prediction_data):
    """Save prediction to file"""
    try:
        all_predictions = {}
        if os.path.exists(PREDICTIONS_FILE):
            with open(PREDICTIONS_FILE, 'r') as f:
                all_predictions = json.load(f)
        
        if username not in all_predictions:
            all_predictions[username] = []
        
        prediction_data['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        all_predictions[username].append(prediction_data)
        
        with open(PREDICTIONS_FILE, 'w') as f:
            json.dump(all_predictions, f, indent=2)
        return True
    except Exception as e:
        print(f"Error saving prediction: {e}")
        return False

# Load users into memory
users = load_users()

def validate_password(password):
    """Validate password requirements (minimum 6 characters)"""
    return 6 <= len(password) <= 50

def validate_username(username):
    """Validate username requirements"""
    return 3 <= len(username) <= 20 and all(c.isalnum() or c in '_-' for c in username)

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
    """Redirect to home if logged in, otherwise to login"""
    if 'user' not in session:
        return redirect(url_for('login'))
    return redirect(url_for('home'))

@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login"""
    error = None
    register_mode = request.args.get('register') == 'true'
    
    if request.method == "POST":
        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")
        
        if not username or not password:
            error = "❌ Please enter both username and password"
        elif username not in users:
            error = "❌ Username not found. Please register first."
        elif users[username] != password:
            error = "❌ Invalid password. Please try again."
        else:
            session['user'] = username
            return redirect(url_for('home'))
    
    return render_template("login.html", error=error, register_mode=register_mode)

@app.route("/register", methods=["POST"])
def register():
    """Handle user registration"""
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")
    confirm_password = request.form.get("confirm_password", "")
    
    error = None
    
    # Validation checks
    if not username:
        error = "❌ Username cannot be empty"
    elif not validate_username(username):
        error = "❌ Username must be 3-20 characters (letters, numbers, - or _)"
    elif username in users:
        error = "❌ Username already exists. Please choose another."
    elif not password:
        error = "❌ Password cannot be empty"
    elif not validate_password(password):
        error = "❌ Password must be 6-50 characters"
    elif password != confirm_password:
        error = "❌ Passwords do not match"
    
    if error:
        return render_template("login.html", error=error, register_mode=True)
    
    # Register user
    users[username] = password
    if save_users(users):
        session['user'] = username
        return redirect(url_for('home'))
    else:
        return render_template("login.html", 
                             error="❌ Error creating account. Please try again.", 
                             register_mode=True)

@app.route("/home")
@login_required
def home():
    """Home page with prediction form"""
    username = session.get('user')
    predictions = load_predictions(username)
    return render_template("index.html", 
                         username=username,
                         prediction_count=len(predictions))

@app.route("/predict", methods=["POST"])
@login_required
def predict():
    """Make diabetes prediction"""
    username = session.get('user')
    
    if model is None or scaler is None:
        return render_template("index.html", 
                             error="❌ Prediction model not loaded. Please contact administrator.", 
                             username=username)
    
    try:
        # Get form data
        pregnancies = float(request.form.get("pregnancies", 0))
        glucose = float(request.form.get("glucose", 0))
        bloodpressure = float(request.form.get("bloodpressure", 0))
        skinthickness = float(request.form.get("skinthickness", 0))
        insulin = float(request.form.get("insulin", 0))
        bmi = float(request.form.get("bmi", 0))
        dpf = float(request.form.get("dpf", 0))
        age = float(request.form.get("age", 0))

        # Validate inputs
        if glucose <= 0 or age <= 0 or bmi <= 0:
            return render_template("index.html", 
                                 error="❌ Please enter valid positive values for glucose, age, and BMI", 
                                 username=username)
        
        if pregnancies < 0 or bloodpressure < 0 or skinthickness < 0 or insulin < 0 or dpf < 0:
            return render_template("index.html", 
                                 error="❌ Please enter valid non-negative values", 
                                 username=username)

        # Prepare data for prediction
        data = np.array([[pregnancies, glucose, bloodpressure, skinthickness, 
                         insulin, bmi, dpf, age]])

        # Scale data
        data_scaled = scaler.transform(data)

        # Make prediction
        prediction = model.predict(data_scaled)[0]
        probability = model.predict_proba(data_scaled)[0][1] * 100

        # Determine result
        if prediction == 1:
            result = "Diabetic"
            if probability > 75:
                risk_level = "🔴 High Risk"
                risk_color = "danger"
            elif probability > 50:
                risk_level = "🟡 Medium Risk"
                risk_color = "warning"
            else:
                risk_level = "🟢 Low Risk"
                risk_color = "success"
        else:
            result = "Non-Diabetic"
            risk_level = "🟢 Low Risk"
            risk_color = "success"

        # Save prediction
        prediction_data = {
            "result": result,
            "probability": round(probability, 2),
            "risk_level": risk_level,
            "pregnancies": pregnancies,
            "glucose": glucose,
            "bloodpressure": bloodpressure,
            "skinthickness": skinthickness,
            "insulin": insulin,
            "bmi": bmi,
            "dpf": dpf,
            "age": age
        }
        save_prediction(username, prediction_data)

        return render_template("result.html",
                             prediction=result,
                             probability=round(probability, 2),
                             risk_level=risk_level,
                             risk_color=risk_color,
                             username=username,
                             pregnancies=pregnancies,
                             glucose=glucose,
                             bloodpressure=bloodpressure,
                             skinthickness=skinthickness,
                             insulin=insulin,
                             bmi=bmi,
                             dpf=dpf,
                             age=age)
        
    except ValueError as e:
        return render_template("index.html", 
                             error="❌ Please enter valid numerical values for all fields", 
                             username=username)
    except Exception as e:
        print(f"Prediction error: {e}")
        return render_template("index.html", 
                             error=f"❌ An error occurred: {str(e)}", 
                             username=username)

@app.route("/history")
@login_required
def history():
    """View prediction history"""
    username = session.get('user')
    predictions = load_predictions(username)
    # Reverse to show newest first
    predictions.reverse()
    return render_template("history.html", 
                         username=username,
                         predictions=predictions,
                         prediction_count=len(predictions))

@app.route("/logout")
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))

@app.route("/health-tips")
@login_required
def health_tips():
    """Health tips and recommendations"""
    return render_template("health_tips.html", username=session.get('user'))

@app.route("/diet-recommendations")
@login_required
def diet_recommendations():
    """Diet recommendations"""
    return render_template("diet_recommendations.html", username=session.get('user'))

@app.route("/exercise-guide")
@login_required
def exercise_guide():
    """Exercise guide"""
    return render_template("exercise_guide.html", username=session.get('user'))

@app.route("/risk-assessment")
@login_required
def risk_assessment():
    """Risk assessment information"""
    return render_template("risk_assessment.html", username=session.get('user'))

@app.route("/about")
@login_required
def about():
    """About the system"""
    return render_template("about.html", username=session.get('user'))

@app.route("/bmi-calculator")
@login_required
def bmi_calculator():
    """BMI calculator"""
    return render_template("bmi_calculator.html", username=session.get('user'))

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template("404.html"), 404

@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors"""
    return render_template("500.html"), 500

if __name__ == "__main__":
    # Development settings
    app.run(debug=True, host='0.0.0.0', port=5000)