import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# Load dataset
df = pd.read_csv("dataset/creditcard.csv")

print("Dataset loaded successfully!")

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nDataset information:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

print("\nClass distribution:")
print(df["Class"].value_counts())

print("\nClass distribution percentage:")
print(df["Class"].value_counts(normalize=True) * 100)

# plt.figure(figsize=(7, 5))

# sns.countplot(
#     x="Class",
#     data=df
# )

# plt.title("Distribution of Legitimate and Fraudulent Transactions")
# plt.xlabel("Class")
# plt.ylabel("Number of Transactions")

# plt.xticks(
#     [0, 1],
#     ["Legitimate", "Fraud"]
# )

# plt.show()


print("\nAmount statistics:")
print(df["Amount"].describe())

# plt.figure(figsize=(10, 5))

# sns.histplot(
#     df["Amount"],
#     bins=50,
#     kde=True
# )

# plt.title("Distribution of Transaction Amount")
# plt.xlabel("Transaction Amount")
# plt.ylabel("Frequency")

# plt.show()

# plt.figure(figsize=(10, 5))

# sns.boxplot(
#     x="Class",
#     y="Amount",
#     data=df
# )

# plt.title("Transaction Amount by Class")
# plt.xticks(
#     [0, 1],
#     ["Legitimate", "Fraud"]
# )

# plt.show()

# plt.figure(figsize=(10, 5))

# sns.boxplot(
#     x="Class",
#     y="Time",
#     data=df
# )

# plt.title("Transaction Time by Class")

# plt.xticks(
#     [0, 1],
#     ["Legitimate", "Fraud"]
# )

# plt.show()

# Check correlation btw each feature
correlation = df.corr()["Class"].sort_values(
    ascending=False
)

print("\nCorrelation with Class:")
print(correlation)

# Correlation heatmap
plt.figure(figsize=(14, 10))

sns.heatmap(
    df.corr(),
    cmap="coolwarm",
    center=0
)

plt.title("Feature Correlation Heatmap")

plt.show()