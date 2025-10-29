from flask import Flask, render_template, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)
import os
model = pickle.load(open(os.path.join("models", "AQI_model.pkl"), "rb"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = [float(request.form[key]) for key in ["pm25", "pm10", "no2", "so2", "co", "o3"]]
        prediction = model.predict([data])[0]
        prediction = max(0, round(prediction, 2))  # No negative AQI

        if prediction <= 50:
            category = "Good"
            css_class = "good"
        elif prediction <= 100:
            category = "Satisfactory"
            css_class = "satisfactory"
        elif prediction <= 200:
            category = "Moderate"
            css_class = "moderate"
        elif prediction <= 300:
            category = "Poor"
            css_class = "poor"
        elif prediction <= 400:
            category = "Very Poor"
            css_class = "very-poor"
        else:
            category = "Severe"
            css_class = "severe"

        return render_template("index.html", aqi=prediction, category=category, css_class=css_class)

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
