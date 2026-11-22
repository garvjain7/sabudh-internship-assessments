import os
import runpy
import joblib
import pandas as pd
from flask import Flask, jsonify, request

# build the model first if task 3/4 have not been run yet
if not os.path.exists("best_model.joblib"):
    for script in ("task3_tuning.py", "task4_model_selection.py"):
        runpy.run_path(script)

# model bundle saved by task4_model_selection.py
bundle = joblib.load("best_model.joblib")
model, FEATURES = bundle["model"], bundle["features"]

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify(status="ok", model=bundle["name"], features=FEATURES)


@app.post("/predict")
def predict():
    body = request.get_json(silent=True)
    if body is None:
        return jsonify(error="send a JSON body"), 400
    rows = body if isinstance(body, list) else [body]
    missing = sorted({f for r in rows for f in FEATURES if f not in r})
    if missing:
        return jsonify(error="missing fields", fields=missing), 400
    try:
        X = pd.DataFrame(rows)[FEATURES].astype(float)
    except (ValueError, TypeError):
        return jsonify(error="all feature values must be numeric"), 400
    preds = model.predict(X)
    return jsonify(predicted_market_value=[round(float(p), 2) for p in preds])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)