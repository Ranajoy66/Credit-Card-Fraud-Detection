import joblib
import pandas as pd

model = joblib.load(
    "models/fraud_detection_model.pkl"
)

scaler = joblib.load(
    "models/scaler.pkl"
)

df = pd.read_csv(
    "dataset/creditcard.csv"
)

X = df.drop(
    "Class",
    axis=1
)

y = df["Class"]

test_transactions = X.iloc[:20]
test_scaled = scaler.transform(
    test_transactions
)
predictions = model.predict(
    test_scaled
)

probabilities = model.predict_proba(
    test_scaled
)[:, 1]
for i, (prediction, probability) in enumerate(
    zip(predictions, probabilities)
):

    if prediction == 1:
        status = "FRAUD"
    else:
        status = "LEGITIMATE"

    print(
        f"Transaction {i + 1}: "
        f"{status} | "
        f"Fraud Probability: {probability:.4f}"
    )