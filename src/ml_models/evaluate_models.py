import pandas as pd
import numpy as np
import os
import logging
import joblib
from sklearn.metrics import (
    f1_score,
    accuracy_score,
    precision_score,
    recall_score,
    roc_auc_score,
    classification_report,
    confusion_matrix,
)
from typing import Dict, List, Tuple

logger = logging.getLogger(__name__)


MODEL_PATHS = {
    "logistic_regression": "models/logistic_regression.pkl",
    "random_forest": "models/random_forest.pkl",
    "xgboost": "models/xgboost_classifier.json",
    "lightgbm": "models/lightgbm_classifier.pkl",
    "catboost": "models/catboost_classifier.cbm",
    "svm": "models/svm_classifier.pkl",
    "naive_bayes": "models/naive_bayes.pkl",
    "knn": "models/knn_classifier.pkl",
    "decision_tree": "models/decision_tree.pkl",
    "adaboost": "models/adaboost.pkl",
    "gradient_boosting": "models/gradient_boosting.pkl",
    "extra_trees": "models/extra_trees.pkl",
}

NEEDS_SCALER = ["svm", "knn", "naive_bayes"]


def load_model(name: str):
    """Load model by name."""
    path = MODEL_PATHS.get(name)
    if path and os.path.exists(path):
        try:
            if name == "xgboost":
                import xgboost as xgb

                model = xgb.XGBClassifier()
                model.load_model(path)
                return model
            elif name == "catboost":
                from catboost import CatBoostClassifier

                model = CatBoostClassifier()
                model.load_model(path)
                return model
            else:
                return joblib.load(path)
        except Exception as e:
            logger.warning(f"Could not load {name}: {e}")
            return None
    return None


def load_scaler(name: str):
    """Load scaler for models that need it."""
    scaler_path = f"models/{name}_scaler.pkl"
    if os.path.exists(scaler_path):
        return joblib.load(scaler_path)
    return None


def evaluate_single_model(
    model_name: str, X_val: pd.DataFrame, y_val: pd.Series
) -> Dict:
    """Evaluate a single model."""
    model = load_model(model_name)

    if model is None:
        return {
            "model": model_name,
            "accuracy": 0,
            "f1": 0,
            "precision": 0,
            "recall": 0,
            "roc_auc": 0,
            "error": "Model not found",
        }

    X_processed = X_val.fillna(0)

    if model_name in NEEDS_SCALER:
        scaler = load_scaler(model_name)
        if scaler:
            X_processed = scaler.transform(X_processed)

    try:
        y_pred = model.predict(X_processed)
        y_proba = model.predict_proba(X_processed)[:, 1]

        return {
            "model": model_name,
            "accuracy": accuracy_score(y_val, y_pred),
            "f1": f1_score(y_val, y_pred),
            "precision": precision_score(y_val, y_pred, zero_division=0),
            "recall": recall_score(y_val, y_pred, zero_division=0),
            "roc_auc": roc_auc_score(y_val, y_proba),
        }
    except Exception as e:
        logger.error(f"Error evaluating {model_name}: {e}")
        return {
            "model": model_name,
            "accuracy": 0,
            "f1": 0,
            "precision": 0,
            "recall": 0,
            "roc_auc": 0,
            "error": str(e),
        }


def evaluate_all_models(X_val: pd.DataFrame, y_val: pd.Series) -> pd.DataFrame:
    """Evaluate all trained models."""
    results = []

    for model_name in MODEL_PATHS.keys():
        logger.info(f"Evaluating {model_name}...")
        metrics = evaluate_single_model(model_name, X_val, y_val)
        results.append(metrics)

    results_df = pd.DataFrame(results)
    results_df = results_df.sort_values("f1", ascending=False)

    return results_df


def get_best_model(results_df: pd.DataFrame, metric: str = "f1") -> str:
    """Get the best model name based on a metric."""
    if results_df.empty:
        return "N/A"

    if "error" in results_df.columns:
        valid_results = results_df[results_df["error"].isna()]
        if valid_results.empty:
            return "N/A"
        return valid_results.iloc[0]["model"]

    return results_df.iloc[0]["model"]


def create_comparison_table(results_df: pd.DataFrame) -> str:
    """Create a formatted comparison table."""
    if results_df.empty:
        return "No results available"

    table = "\n=== Model Comparison ===\n"
    table += f"{'Model':<25} {'Accuracy':<10} {'F1':<10} {'Precision':<10} {'Recall':<10} {'ROC-AUC':<10}\n"
    table += "-" * 75 + "\n"

    for _, row in results_df.iterrows():
        table += f"{row['model']:<25} {row['accuracy']:.4f}   {row['f1']:.4f}   {row['precision']:.4f}   {row['recall']:.4f}   {row['roc_auc']:.4f}\n"

    return table


def run_evaluation() -> pd.DataFrame:
    """Run full model evaluation."""

    try:
        X_val = pd.read_csv("data/ml/X_val.csv")
        y_val = pd.read_csv("data/ml/y_val_class.csv")["is_delayed"]
    except Exception as e:
        logger.warning(f"Could not load validation data: {e}. Using sample data.")
        np.random.seed(42)
        X_val = pd.DataFrame(
            {
                "feature1": np.random.randn(200),
                "feature2": np.random.randn(200),
                "feature3": np.random.randint(0, 5, 200),
                "feature4": np.random.randn(200),
                "feature5": np.random.randn(200),
            }
        )
        y_val = pd.Series(np.random.randint(0, 2, 200))

    results_df = evaluate_all_models(X_val, y_val)

    os.makedirs("data/ml", exist_ok=True)
    results_df.to_csv("data/ml/classification_results.csv", index=False)

    print(create_comparison_table(results_df))

    best_model = get_best_model(results_df)
    print(f"\nBest model (by F1): {best_model}")

    return results_df


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    results = run_evaluation()
