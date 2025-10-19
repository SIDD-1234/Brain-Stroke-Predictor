from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle
import numpy as np
import requests
import json

app = Flask(__name__)

# ===== Load CSV and Model =====
df = pd.read_csv("brain_stroke.csv")

try:
    model_data = pickle.load(open("stroke_model.pkl", "rb"))
    model = model_data["model"]
    encoders = model_data["encoders"]
    model_columns = model_data["columns"]
except Exception as e:
    model, encoders, model_columns = None, {}, []
    print(f"⚠️ Model load failed: {e}")

# ===== Helper Functions =====
def prepare_input(data):
    """Convert user input dict to DataFrame with correct order/columns"""
    input_df = pd.DataFrame([data])

    # Convert 'Yes'/'No' for hypertension and heart_disease
    yes_no_map = {"Yes": 1, "No": 0, "yes": 1, "no": 0}
    for col in ["hypertension", "heart_disease"]:
        if col in input_df.columns:
            input_df[col] = input_df[col].replace(yes_no_map)

    # Convert numeric columns if needed
    for col in input_df.columns:
        try:
            input_df[col] = pd.to_numeric(input_df[col])
        except:
            pass

    return input_df


# ===== Routes =====
@app.route("/")
def dashboard():
    return render_template("dashboard.html")


@app.route("/form")
def form_page():
    columns = [col for col in df.columns if col != "stroke"]
    # Map categorical choices for dropdowns
    choices = {
        "gender": df["gender"].dropna().unique().tolist(),
        "ever_married": df["ever_married"].dropna().unique().tolist(),
        "work_type": df["work_type"].dropna().unique().tolist(),
        "Residence_type": df["Residence_type"].dropna().unique().tolist(),
        "smoking_status": df["smoking_status"].dropna().unique().tolist(),
    }
    return render_template("form.html", columns=columns, choices=choices)


@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json()
        input_df = prepare_input(data)

        # Apply label encoders
        for col, le in encoders.items():
            if col in input_df.columns:
                try:
                    input_df[col] = le.transform(input_df[col])
                except ValueError:
                    input_df[col] = [le.classes_[0]]  # fallback

        input_df = input_df.reindex(columns=model_columns, fill_value=0)

        prob = float(model.predict_proba(input_df)[0][1])
        result = int(model.predict(input_df)[0])

        return jsonify({
            "prediction": result,
            "probability": prob
        })
    except Exception as e:
        print("Prediction error:", e)
        return jsonify({"error": "Prediction failed"}), 500


@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    body = request.json or {}
    inputs = body.get('inputs', {})

    prompt = (
        "You are a friendly, non-diagnostic health assistant. "
        "Based on the following patient details, suggest 3-5 practical, evidence-informed steps "
        "to reduce stroke risk and list any red flags requiring immediate medical attention. "
        "Keep it short in less than 50 words as a summarized version and encouraging."
        f"{inputs}"
    )

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma3:4b", "prompt": prompt, "stream": False},
            timeout=120
        )

        text = response.text.strip()
        data = json.loads(text.split("\n")[-1]) if "\n" in text else response.json()
        ai_text = data.get("response", "").strip() or "⚠️ No advice generated."
        return jsonify({"ai_response": ai_text})

    except requests.exceptions.RequestException as e:
        return jsonify({"ai_response": f"⚠️ Request failed: {str(e)}"})


@app.route("/statistics")
def statistics():
    return render_template("statistics.html")


@app.route("/stats_data/<attribute>")
def stats_data(attribute):
    """Return counts for bar chart: attribute vs stroke"""
    try:
        grouped = df.groupby([attribute, "stroke"]).size().unstack(fill_value=0)
        labels = grouped.index.tolist()
        stroke = grouped[1].tolist() if 1 in grouped.columns else [0]*len(labels)
        no_stroke = grouped[0].tolist() if 0 in grouped.columns else [0]*len(labels)
        return jsonify({
            "labels": [str(l) for l in labels],
            "stroke": stroke,
            "no_stroke": no_stroke
        })
    except Exception as e:
        print("Stats error:", e)
        return jsonify({"error": "Invalid attribute"}), 400


@app.route("/get_fact")
def get_fact():
    """Fetch a random stroke/health fact from Ollama (gemma3:4b)"""
    try:
        prompt = "Tell me a short, interesting medical or health fact or statistics about stroke or brain health. In one line only make it new everytime when i ask"
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "gemma3:4b", "prompt": prompt, "stream": False},
            timeout=60
        )
        data = response.json()
        fact = data.get("response", "").strip()
        return jsonify({"fact": fact or "⚠️ No fact generated."})
    except Exception as e:
        print("Fact fetch error:", e)
        return jsonify({"fact": f"⚠️ Could not connect to Ollama. ({str(e)})"})


if __name__ == "__main__":
    app.run(debug=True)
