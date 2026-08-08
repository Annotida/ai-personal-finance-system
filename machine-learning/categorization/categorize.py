"""
Transaction categorization model.

Loads a trained TF-IDF + Logistic Regression model and provides a single
function, predict_category(), that takes a transaction description and
returns its predicted spending category.
"""

import joblib

_artifacts = joblib.load("categorizer.joblib")
vectorizer = _artifacts["vectorizer"]
model = _artifacts["model"]


def predict_category(text: str) -> str:
    """Predict the spending category for a transaction description."""
    vec = vectorizer.transform([text])
    return model.predict(vec)[0]


if __name__ == "__main__":
    examples = [
        "UBER EATS ORDER #4821",
        "SHELL GAS STATION",
        "NETFLIX.COM",
    ]
    for text in examples:
        print(f"{text:30} -> {predict_category(text)}")
