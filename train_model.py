import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import lightgbm as lgb
import joblib

# === CHOOSE DATASET ===
#DATASET_PATH = "iot_real_dataset.csv"   # or "iot_synthetic_dataset_5000.csv"
DATASET_PATH = "iotDataSet.csv"   # or "iot_synthetic_dataset_5000.csv"


# Load dataset
df = pd.read_csv(DATASET_PATH)
print("✅ Dataset loaded. Shape:", df.shape)

# Fix rows with no ports open as "Safe"
port_cols = [c for c in df.columns if c.startswith("port_")]
df.loc[df[port_cols].sum(axis=1) == 0, "risk_label"] = "Safe"

# Feature/label split
X = df.drop("risk_label", axis=1)
y = df["risk_label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

results = {}

# === Random Forest ===
print("\n🌲 Training Random Forest...")
rf_model = RandomForestClassifier(n_estimators=200, random_state=42)
rf_model.fit(X_train, y_train)
y_pred_rf = rf_model.predict(X_test)

results["Random Forest"] = accuracy_score(y_test, y_pred_rf)
print("Random Forest Accuracy:", results["Random Forest"])
print(classification_report(y_test, y_pred_rf))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_rf))

# === LightGBM ===
print("\n💡 Training LightGBM...")
lgb_model = lgb.LGBMClassifier(
    n_estimators=200,
    learning_rate=0.1,
    max_depth=-1,
    random_state=42
)
lgb_model.fit(X_train, y_train)
y_pred_lgb = lgb_model.predict(X_test)

results["LightGBM"] = accuracy_score(y_test, y_pred_lgb)
print("LightGBM Accuracy:", results["LightGBM"])
print(classification_report(y_test, y_pred_lgb))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred_lgb))

# === Isolation Forest (Unsupervised) ===
print("\n🕵️ Training Isolation Forest (Anomaly Detection)...")
iso_model = IsolationForest(contamination=0.1, random_state=42)
iso_model.fit(X_train)

# Predict anomalies (-1 = anomaly, 1 = normal)
y_pred_iso = iso_model.predict(X_test)

# Map predictions to labels for evaluation
y_pred_iso_labels = ["Safe" if p == 1 else "Attack" for p in y_pred_iso]
y_true_iso_labels = ["Safe" if label == "Safe" else "Attack" for label in y_test]

results["Isolation Forest"] = accuracy_score(y_true_iso_labels, y_pred_iso_labels)
print("Isolation Forest Accuracy:", results["Isolation Forest"])
print(classification_report(y_true_iso_labels, y_pred_iso_labels))

# === Choose Best Supervised Model (RF vs LightGBM) ===
best_model_name = max(["Random Forest", "LightGBM"], key=lambda k: results[k])
best_model = rf_model if best_model_name == "Random Forest" else lgb_model

joblib.dump(best_model, "model.pkl")
print(f"\n✅ Best model ({best_model_name}) saved as model.pkl")


import matplotlib.pyplot as plt

# --- Calculate train accuracy for each model ---
# Random Forest
train_acc_rf = accuracy_score(y_train, rf_model.predict(X_train))
test_acc_rf = accuracy_score(y_test, y_pred_rf)

# LightGBM
train_acc_lgb = accuracy_score(y_train, lgb_model.predict(X_train))
test_acc_lgb = accuracy_score(y_test, y_pred_lgb)

# Store results
train_acc = {
    "Random Forest": train_acc_rf,
    "LightGBM": train_acc_lgb
}
test_acc = {
    "Random Forest": test_acc_rf,
    "LightGBM": test_acc_lgb
}

# --- Plot comparison graph ---
models = list(train_acc.keys())
x = range(len(models))

plt.figure(figsize=(8,5))
plt.bar(x, [train_acc[m] for m in models], width=0.4, label="Train Accuracy", align="center")
plt.bar([i+0.4 for i in x], [test_acc[m] for m in models], width=0.4, label="Test Accuracy", align="center")

plt.xticks([i+0.2 for i in x], models)
plt.ylabel("Accuracy")
plt.ylim(0, 1.05)
plt.title("Train vs Test Accuracy (Overfitting Check)")
plt.legend()
plt.show()
