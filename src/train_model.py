import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import (
    classification_report,
    confusion_matrix,
    roc_auc_score
)
from sklearn.metrics import roc_curve


# Load dataset
df = pd.read_csv("dataset/creditcard.csv")

print("Dataset loaded successfully!")

X = df.drop("Class", axis=1)
y = df["Class"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("Training data:", X_train.shape)
print("Testing data:", X_test.shape)


scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)


smote = SMOTE(
    random_state=42
)

X_train_resampled, y_train_resampled = smote.fit_resample(
    X_train_scaled,
    y_train
)

print("Before SMOTE:")
print(y_train.value_counts())

print("\nAfter SMOTE:")
print(y_train_resampled.value_counts())

# Convert scaled + SMOTE data to DataFrame
X_train_smote_df = pd.DataFrame(
    X_train_resampled,
    columns=X.columns
)
# Add target column
X_train_smote_df["Class"] = y_train_resampled.values

# Save to CSV
X_train_smote_df.to_csv(
    "dataset/creditcard_smote_scaled.csv",
    index=False
)

print("SMOTE + scaled dataset saved successfully!")

# model training
model = LogisticRegression(
    max_iter=1000,
    random_state=42
)

model.fit(
    X_train_resampled,
    y_train_resampled
)

print("Model training completed!")

y_pred = model.predict(X_test_scaled)
y_prob = model.predict_proba(
    X_test_scaled
)[:, 1]

roc_auc = roc_auc_score(
    y_test,
    y_prob
)

print("ROC-AUC:", roc_auc)

print("\nClassification Report:")
print(
    classification_report(
        y_test,
        y_pred
    )
)

cm = confusion_matrix(
    y_test,
    y_pred
)

print("\nConfusion Matrix:")
print(cm)

# plt.figure(figsize=(7, 5))

# sns.heatmap(
#     cm,
#     annot=True,
#     fmt="d",
#     cmap="Blues",
#     xticklabels=["Legitimate", "Fraud"],
#     yticklabels=["Legitimate", "Fraud"]
# )

# plt.xlabel("Predicted")
# plt.ylabel("Actual")
# plt.title("Fraud Detection Confusion Matrix")

# plt.show()

# ROC-AUC curve
# fpr, tpr, thresholds = roc_curve(
#     y_test,
#     y_prob
# )

# plt.figure(figsize=(8, 6))

# plt.plot(
#     fpr,
#     tpr,
#     label=f"Logistic Regression (AUC = {roc_auc:.4f})"
# )

# plt.plot(
#     [0, 1],
#     [0, 1],
#     linestyle="--"
# )

# plt.xlabel("False Positive Rate")
# plt.ylabel("True Positive Rate")

# plt.title("ROC Curve")

# plt.legend()

# plt.show()

# saving trained our model
import joblib

joblib.dump(
    model,
    "models/fraud_detection_model.pkl"
)

joblib.dump(
    scaler,
    "models/scaler.pkl"
)

print("Model and scaler saved successfully.")