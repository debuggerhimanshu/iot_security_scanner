# graphs.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import lightgbm as lgb

# === Load Dataset ===
DATASET_PATH = "iotDataSet.csv"
df = pd.read_csv(DATASET_PATH)

# Fix rows with no ports open as "Safe"
port_cols = [c for c in df.columns if c.startswith("port_")]
df.loc[df[port_cols].sum(axis=1) == 0, "risk_label"] = "Safe"

X = df.drop("risk_label", axis=1)
y = df["risk_label"]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

# === Random Forest ===
print("\n🌲 Training Random Forest...")
rf = RandomForestClassifier(n_estimators=200, random_state=42)
rf.fit(X_train, y_train)
y_pred_rf = rf.predict(X_test)
acc_rf = accuracy_score(y_test, y_pred_rf)

# === LightGBM ===
print("\n💡 Training LightGBM...")
lgb_model = lgb.LGBMClassifier(n_estimators=200, learning_rate=0.1, random_state=42)
lgb_model.fit(X_train, y_train)
y_pred_lgb = lgb_model.predict(X_test)
acc_lgb = accuracy_score(y_test, y_pred_lgb)

# === 1. Accuracy Comparison ===
models = ["Random Forest", "LightGBM"]
accuracies = [acc_rf, acc_lgb]

plt.figure(figsize=(7,5))
sns.barplot(x=models, y=accuracies, palette="viridis")
plt.ylim(0,1.05)
plt.ylabel("Accuracy")
plt.title("Model Accuracy Comparison")
plt.savefig("accuracy_comparison.png")
plt.show()

# === 2. Confusion Matrix (Random Forest) ===
cm_rf = confusion_matrix(y_test, y_pred_rf, labels=rf.classes_)
plt.figure(figsize=(7,5))
sns.heatmap(cm_rf, annot=True, fmt="d", cmap="Blues",
            xticklabels=rf.classes_, yticklabels=rf.classes_)
plt.title("Confusion Matrix (Random Forest)")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.savefig("confusion_matrix_rf.png")
plt.show()

# === 3. Confusion Matrix (LightGBM) ===
cm_lgb = confusion_matrix(y_test, y_pred_lgb, labels=lgb_model.classes_)
plt.figure(figsize=(7,5))
sns.heatmap(cm_lgb, annot=True, fmt="d", cmap="Greens",
            xticklabels=lgb_model.classes_, yticklabels=lgb_model.classes_)
plt.title("Confusion Matrix (LightGBM)")
plt.xlabel("Predicted")
plt.ylabel("True")
plt.savefig("confusion_matrix_lgb.png")
plt.show()

# === 4. Classification Report (Random Forest) ===
report_rf = classification_report(y_test, y_pred_rf, output_dict=True)
df_report_rf = pd.DataFrame(report_rf).transpose()
plt.figure(figsize=(8,5))
sns.heatmap(df_report_rf.iloc[:-1, :-1], annot=True, cmap="YlGnBu", fmt=".2f")
plt.title("Classification Report (Random Forest)")
plt.savefig("classification_report_rf.png")
plt.show()

# === 5. Classification Report (LightGBM) ===
report_lgb = classification_report(y_test, y_pred_lgb, output_dict=True)
df_report_lgb = pd.DataFrame(report_lgb).transpose()
plt.figure(figsize=(8,5))
sns.heatmap(df_report_lgb.iloc[:-1, :-1], annot=True, cmap="Oranges", fmt=".2f")
plt.title("Classification Report (LightGBM)")
plt.savefig("classification_report_lgb.png")
plt.show()

# === 6. Risk Label Distribution ===
plt.figure(figsize=(6,5))
df["risk_label"].value_counts().plot(kind="bar", color="orange")
plt.title("Risk Label Distribution in Dataset")
plt.ylabel("Count")
plt.savefig("risk_label_distribution.png")
plt.show()
