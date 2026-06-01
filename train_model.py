import pandas as pd
import pickle

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
data = pd.read_csv("data/training_data.csv")

# Features and labels
X = data["text"]
y = data["category"]

# Convert text into vectors
vectorizer = TfidfVectorizer()

X_vectors = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression()

model.fit(X_vectors, y)

# Save model
with open("model.pkl", "wb") as model_file:
    pickle.dump(model, model_file)

# Save vectorizer
with open("vectorizer.pkl", "wb") as vec_file:
    pickle.dump(vectorizer, vec_file)

print("Model trained successfully!")