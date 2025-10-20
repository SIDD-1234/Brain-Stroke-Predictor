# Brain-Stroke-Predictor

An interactive web application built with **Flask**, **Machine Learning**, and **Ollama (Gemma 3:4B)** to predict the risk of brain stroke based on health attributes.  
It also provides **AI-generated preventive advice** and **health facts** fetched locally using Ollama.

## Screenshots

| Dashboard | Prediction Form | Statistics |
|------------|------------------|-------------|
| ![Dashboard Screenshot](assets/dashboard.png) | ![Form Screenshot](assets/form.png) | ![Statistics Screenshot](assets/statistics.png) |

## Features

- **User-friendly stroke prediction form** with dropdowns and inputs.
- **AI Advice Generator** using **Gemma 3:4B** via **Ollama** (offline, local AI).
- **Statistical Visualization** for dataset attributes (stroke vs factors).
- **Dynamic Health Facts** — fetches a new fact each time you load.
- **Interactive Frontend** built with Bootstrap and custom JS.
- **Trained Machine Learning Model (Random Forest)** for prediction.

## Technologies Used

| Category | Tools / Libraries |
|-----------|-------------------|
| **Frontend** | HTML, CSS (Bootstrap), JavaScript |
| **Backend** | Flask (Python) |
| **Machine Learning** | scikit-learn, pandas, numpy |
| **AI Assistant** | Ollama + Gemma 3:4B |
| **Visualization** | Chart.js |
| **Model File** | stroke_model.pkl (pre-trained Random Forest Classifier) |

## Models Tested

| Model | Accuracy | Precision | Recall | F1 Score |
|--------|-----------|------------|---------|-----------|
| Logistic Regression | 0.9458 | 0.0000 | 0.0000 | 0.0000 |
| Decision Tree | 0.9197 | 0.2174 | 0.1851 | 0.2000 |
| **Random Forest (Selected)** | **0.9408** | **0.0000** | **0.0000** | **0.0000** |
| KNN | 0.9418 | 0.1666 | 0.0185 | 0.0333 |
| SVM | 0.9458 | 0.0000 | 0.0000 | 0.0000 |

The **Random Forest Classifier** was chosen for its **balanced accuracy, interpretability, and robustness** on the dataset.

## AI Integration (Ollama)

This project uses **Ollama** to run the **Gemma 3:4B** model locally.  
It provides:
- Dynamic health facts (`/get_fact` route)
- Preventive AI advice (`/ask_ai` route)

### Start Ollama
Make sure Ollama is running locally:
Initialize ollama in another terminal
```bash
ollama run < model name >
```

## Steps to Run the Project

Follow these steps to set up and run the Brain Stroke Risk Predictor on your system.

### 1. Prepare the Dataset
- Ensure that `brain_stroke.csv` is present in the project root directory.  
- The dataset should contain the following key columns:

```bash
gender, age, hypertension, heart_disease, ever_married, work_type,
Residence_type, avg_glucose_level, bmi, smoking_status, stroke
```

### 2. Train the Model
Before running the web app, train and save the model using:
```bash
python train_model.py
```

This script:
- Loads and cleans the dataset
- Encodes categorical columns
- Trains a Random Forest Classifier
- Saves the trained model as stroke_model.pkl

You should see this message after successful training:

```bash
✅ Model saved as stroke_model.pkl
```

### 3. Run the Flask Application
Once the model is ready, start the app:
```bash
python app.py
```

If everything loads correctly, you’ll see:

```bash
Running on http://127.0.0.1:5000/
```

Open the given URL in your browser.

### 4. Use the Interface

Click “Predict Stroke Risk” on the dashboard to open the prediction form.
- Fill in the patient’s details (gender, age, etc.).
- Click “Predict” to see the stroke probability.
- Click “Ask the Internet” to receive AI-generated health advice (via Ollama gemma3:4b model).

### 5. View Statistics
- Navigate to the Statistics Dashboard to view insights such as attribute distribution vs stroke occurrence.

### 6. Enable Ollama AI (Optional)
To generate AI advice or health facts, make sure Ollama is running locally and the gemma3:4b model is installed:

```bash
ollama run gemma3:4b
```

### 7. Test via Postman (Optional)
You can test the prediction API directly using a POST request to:

```bash
http://127.0.0.1:5000/predict
```

With a sample JSON body:

```bash
{
  "gender": "Male",
  "age": 67,
  "hypertension": 1,
  "heart_disease": 0,
  "ever_married": "Yes",
  "work_type": "Private",
  "Residence_type": "Urban",
  "avg_glucose_level": 228.69,
  "bmi": 36.6,
  "smoking_status": "formerly smoked"
}
```
The API will return:
```bash
{
  "prediction": 1,
  "probability": 0.84
}
```
