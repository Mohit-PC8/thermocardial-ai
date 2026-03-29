# 🫀 ThermoCardial AI — Heart Disease Prediction Web App

> Advanced heart disease prediction using **Thermodynamic Attention Regression (TAR)** methodology  
> RandomForest Classifier · 91.75% Accuracy · SQLite Database · Plotly Visualizations

---

## 📁 Project Structure

```
thermocardia/
│
├── app.py                  ← Streamlit frontend (this file)
├── heart_model.pkl         ← Trained RandomForest model  ← YOU MUST PLACE THIS HERE
├── scaler.pkl              ← Fitted StandardScaler        ← YOU MUST PLACE THIS HERE
├── requirements.txt        ← Python dependencies
├── thermocardia.db         ← SQLite DB (auto-created on first run)
└── README.md
```

---

## ⚙️ Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Generate model files (run your training script once)
Ensure `heart_model.pkl` and `scaler.pkl` are in the same folder as `app.py`.  
You can generate them from your Google Colab notebook:
```python
joblib.dump(model, "heart_model.pkl")
joblib.dump(scaler, "scaler.pkl")
```
Then download both files and place them next to `app.py`.

### 3. Run the app
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

---

## 🖥️ Features

| Feature | Description |
|---|---|
| **13-Field Input Form** | All clinical parameters with human-readable labels |
| **Categorical Mappings** | Dropdowns show medical names; numbers sent to model |
| **ℹ️ Info Tooltips** | Click any field header to see description & reference range |
| **Risk Prediction** | High / Medium / Low risk with confidence score |
| **Risk/Protective Factors** | Auto-detected from input values |
| **Radar Chart** | Normalized view of 6 key parameters |
| **Bar Chart** | All 13 raw values visualized |
| **Risk Gauge** | Dial showing cardiac risk probability % |
| **Community Stats** | Live positive vs negative counts from DB |
| **Prediction History** | Last 50 submissions in a table |
| **SQLite Storage** | All inputs + predictions auto-saved |

---

## 🔢 Field Encodings (Reference)

| Field | UI Label | Numeric Value |
|---|---|---|
| **sex** | Female / Male | 0 / 1 |
| **cp** | Typical Angina / Atypical Angina / Non-Anginal / Asymptomatic | 0 / 1 / 2 / 3 |
| **fbs** | No (≤120) / Yes (>120) | 0 / 1 |
| **restecg** | Normal / ST-T Abnormality / LV Hypertrophy | 0 / 1 / 2 |
| **exang** | No / Yes | 0 / 1 |
| **slope** | Upsloping / Flat / Downsloping | 0 / 1 / 2 |
| **ca** | 0–3 Vessels blocked | 0 / 1 / 2 / 3 |
| **thal** | Normal / Fixed Defect / Reversible Defect / Unknown | 0 / 1 / 2 / 3 |

---

## ⚠️ Disclaimer
ThermoCardial AI is for **academic and research purposes only**.  
It is **not** a substitute for professional medical advice or clinical diagnosis.
