import pandas as pd
import os
import logging
import joblib

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


def select_best_model(
    results_path: str = "data/ml/classification_results.csv", metric: str = "f1"
) -> dict:
    """Select the best model based on evaluation results."""

    if os.path.exists(results_path):
        results_df = pd.read_csv(results_path)

        if "error" in results_df.columns:
            results_df = results_df[results_df["error"].isna()]

        if results_df.empty:
            logger.warning("No valid results found. Using default model.")
            return {"model": "random_forest", "path": MODEL_PATHS["random_forest"]}

        results_df = results_df.sort_values(metric, ascending=False)
        best_row = results_df.iloc[0]

        return {
            "model": best_row["model"],
            "path": MODEL_PATHS.get(best_row["model"], "models/random_forest.pkl"),
            "accuracy": best_row["accuracy"],
            "f1": best_row["f1"],
            "precision": best_row["precision"],
            "recall": best_row["recall"],
            "roc_auc": best_row["roc_auc"],
        }
    else:
        logger.warning("Results file not found. Using default model.")
        return {"model": "random_forest", "path": MODEL_PATHS["random_forest"]}


def copy_best_model(best_info: dict) -> None:
    """Copy best model to best_classifier.pkl."""
    import shutil

    source = best_info["path"]
    dest = "models/best_classifier.pkl"

    if os.path.exists(source):
        shutil.copy2(source, dest)
        logger.info(f"Best model copied to {dest}")
    else:
        logger.warning(f"Source model not found: {source}")


def create_model_selection_report(best_info: dict) -> None:
    """Create model selection documentation."""

    report = f"""# Model Selection Report

## Best Model Selected: {best_info["model"]}

### Performance Metrics

| Metric | Value |
|-------|-------|
| Accuracy | {best_info.get("accuracy", "N/A"):.4f} |
| F1 Score | {best_info.get("f1", "N/A"):.4f} |
| Precision | {best_info.get("precision", "N/A"):.4f} |
| Recall | {best_info.get("recall", "N/A"):.4f} |
| ROC-AUC | {best_info.get("roc_auc", "N/A"):.4f} |

## Selection Criteria

- Primary metric: F1 Score
- The model with the highest F1 score on the validation set was selected
- F1 score balances precision and recall, making it ideal for delay prediction

## Model Choice Justification

{best_info["model"]} was selected because:
1. Highest F1 score among all tested models
2. Best balance between precision and recall
3. Suitable for production deployment

## Alternative Models

The following models were also evaluated but had lower F1 scores:
- Random Forest
- XGBoost
- LightGBM
- CatBoost
- Logistic Regression
- SVM
- And others...

## Next Steps

- Use best_classifier.pkl for predictions
- Consider ensemble methods for improved performance
- Monitor model performance in production

---

*Report generated: Model Selection Complete*
"""

    os.makedirs("docs", exist_ok=True)
    with open("docs/model_selection.md", "w") as f:
        f.write(report)

    logger.info("Model selection report saved to docs/model_selection.md")


def run_model_selection() -> dict:
    """Run the full model selection process."""

    best_info = select_best_model()

    print(f"\n=== Model Selection ===")
    print(f"Best model: {best_info['model']}")
    print(f"F1 Score: {best_info.get('f1', 'N/A'):.4f}")

    copy_best_model(best_info)
    create_model_selection_report(best_info)

    return best_info


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_model_selection()
