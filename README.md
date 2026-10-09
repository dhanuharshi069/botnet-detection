# 🛡️ IoT Botnet Attack Detection Using Machine Learning

A machine learning-based web application for analyzing network-flow features and classifying traffic as potentially normal or botnet-related.

## 📌 Project Overview

Internet of Things (IoT) devices can be vulnerable to botnet attacks. This project demonstrates how machine learning can help identify suspicious network-flow patterns and display classification results through a web dashboard.

The application uses a trained Random Forest model, a feature scaler, and a Flask backend with a browser-based interface.

## ✨ Features

- **Traffic Prediction:** Classify network-flow input using the trained model.
- **Batch CSV Prediction:** Upload a CSV file to analyze multiple rows.
- **Threat Classification:** Display predicted labels and confidence values.
- **Attack Feed Simulation:** View sample flow predictions in a simulated feed.
- **Dashboard:** Explore model-related metrics and feature information.
- **Web Interface:** Access the application through a browser.

## 🧰 Technology Stack

- Python
- Flask
- Scikit-learn
- Pandas
- HTML, CSS, and JavaScript
- Joblib
- Ngrok for temporary public access during development

## 📁 Project Structure

```text
botnet-detection/
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── models/
│   ├── random_forest.pkl
│   └── scaler.pkl
├── data/
│   └── sim_data.csv
└── static/
    └── index.html
```

## ⚙️ Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/dhanuharshi069/botnet-detection.git
cd botnet-detection
```

### 2. Create a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start the application

```bash
python app.py
```

Open this address in your browser:

```text
http://127.0.0.1:5000
```

Keep the terminal running while using the application.

## 📊 CSV Input Format

For batch prediction, prepare a CSV file containing these numeric columns:

| Column | Description |
|---|---|
| `Dur` | Flow duration |
| `TotPkts` | Total packet count |
| `TotBytes` | Total bytes |
| `SrcBytes` | Source bytes |

Example:

```csv
Dur,TotPkts,TotBytes,SrcBytes
0.0003,2,203,64
0.0009,2,135,75
1.25,18,1450,820
```

Use feature values and units compatible with those used to train the model.

## 🔍 How It Works

1. The user enters network-flow features or uploads a CSV file.
2. The Flask backend prepares the input for the trained model.
3. The model generates a classification.
4. The dashboard displays the predicted label and associated confidence value.

## ⚠️ Limitations

- Predictions depend on the training data, model quality, and compatibility of input features.
- Sample CSV data and attack-feed simulations are for demonstration and do not represent verified live attacks.
- Live-network functionality should not be considered genuine real-time botnet detection unless actual traffic capture, feature extraction, and model inference are implemented and validated.
- Model performance values should be reported only after evaluation on a documented test dataset.

## 🚀 Future Enhancements

- Integrate validated live network-flow capture.
- Add model evaluation reports and confusion-matrix generation from test data.
- Improve input validation and error handling.
- Add prediction-history storage and downloadable reports.
- Deploy the application on a persistent hosting service.

## 👨‍💻 Author

**Dhanush H S**

GitHub: [@dhanuharshi069](https://github.com/dhanuharshi069)

---

*Academic and demonstration project for IoT network security and machine learning.*
