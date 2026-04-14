import pandas as pd
import numpy as np
import os
import logging
from typing import Dict, List, Tuple, Optional

logger = logging.getLogger(__name__)


def validate_feature_quality(features_dir: str = "data/features") -> pd.DataFrame:
    """Validate feature quality metrics.

    Args:
        features_dir: Directory containing feature CSV files

    Returns:
        DataFrame with quality metrics
    """
    results = []

    if not os.path.exists(features_dir):
        logger.warning(f"Features directory not found: {features_dir}")
        return pd.DataFrame(results)

    for filename in os.listdir(features_dir):
        if not filename.endswith(".csv"):
            continue

        filepath = os.path.join(features_dir, filename)

        try:
            df = pd.read_csv(filepath)

            total_cells = len(df) * len(df.columns)
            null_cells = df.isnull().sum().sum()
            null_pct = (null_cells / total_cells * 100) if total_cells > 0 else 0

            numeric_cols = df.select_dtypes(include=[np.number]).columns
            zero_variance_cols = (
                [c for c in numeric_cols if df[c].nunique() <= 1]
                if len(numeric_cols) > 0
                else []
            )

            results.append(
                {
                    "feature_file": filename,
                    "num_rows": len(df),
                    "num_columns": len(df.columns),
                    "null_count": null_cells,
                    "null_percentage": round(null_pct, 2),
                    "duplicates": df.duplicated().sum(),
                    "zero_variance_features": len(zero_variance_cols),
                    "numeric_features": len(numeric_cols),
                    "categorical_features": len(df.columns) - len(numeric_cols),
                }
            )

        except Exception as e:
            logger.error(f"Error validating {filename}: {e}")
            results.append(
                {
                    "feature_file": filename,
                    "num_rows": 0,
                    "num_columns": 0,
                    "null_count": 0,
                    "null_percentage": 0,
                    "duplicates": 0,
                    "zero_variance_features": 0,
                    "numeric_features": 0,
                    "categorical_features": 0,
                    "error": str(e),
                }
            )

    quality_df = pd.DataFrame(results)
    return quality_df


def check_feature_correlations(
    features_df: pd.DataFrame, target_col: Optional[str] = None, threshold: float = 0.95
) -> Tuple[pd.DataFrame, List[str]]:
    """Check feature correlations and identify high correlation pairs.

    Args:
        features_df: Features dataframe
        target_col: Target column name (optional)
        threshold: Correlation threshold for flagging

    Returns:
        Tuple of (correlation matrix, high correlation pairs)
    """
    numeric_df = features_df.select_dtypes(include=[np.number])

    if numeric_df.empty:
        return pd.DataFrame(), []

    corr_matrix = numeric_df.corr()

    high_corr_pairs = []
    for i in range(len(corr_matrix.columns)):
        for j in range(i + 1, len(corr_matrix.columns)):
            if abs(corr_matrix.iloc[i, j]) > threshold:
                high_corr_pairs.append(
                    {
                        "feature_1": corr_matrix.columns[i],
                        "feature_2": corr_matrix.columns[j],
                        "correlation": round(corr_matrix.iloc[i, j], 3),
                    }
                )

    return corr_matrix, high_corr_pairs


def get_target_correlations(
    features_df: pd.DataFrame, target_col: str = "is_delayed"
) -> pd.Series:
    """Get correlations of features with target.

    Args:
        features_df: Features dataframe
        target_col: Target column name

    Returns:
        Series of correlations with target
    """
    if target_col not in features_df.columns:
        logger.warning(f"Target column {target_col} not found")
        return pd.Series()

    numeric_df = features_df.select_dtypes(include=[np.number])
    if target_col not in numeric_df.columns:
        return pd.Series()

    corr_with_target = (
        numeric_df.corr()[target_col].drop(target_col).sort_values(ascending=False)
    )
    return corr_with_target


def check_feature_distributions(features_df: pd.DataFrame) -> Dict:
    """Check feature distributions for anomalies.

    Args:
        features_df: Features dataframe

    Returns:
        Dictionary of distribution statistics
    """
    numeric_cols = features_df.select_dtypes(include=[np.number]).columns

    stats = {}
    for col in numeric_cols:
        stats[col] = {
            "mean": features_df[col].mean(),
            "median": features_df[col].median(),
            "std": features_df[col].std(),
            "min": features_df[col].min(),
            "max": features_df[col].max(),
            "zeros_pct": (features_df[col] == 0).sum() / len(features_df[col]) * 100
            if len(features_df) > 0
            else 0,
            "null_pct": features_df[col].isnull().sum() / len(features_df[col]) * 100
            if len(features_df) > 0
            else 0,
        }

    return stats


def generate_quality_report(features_dir: str = "data/features") -> Dict:
    """Generate comprehensive quality report.

    Args:
        features_dir: Directory containing feature files

    Returns:
        Dictionary with quality report results
    """
    quality_df = validate_feature_quality(features_dir)

    quality_df.to_csv("data/features/quality_report.csv", index=False)
    logger.info(f"Saved quality report to data/features/quality_report.csv")

    print("\n=== Feature Quality Report ===")
    print(quality_df.to_string(index=False))

    total_nulls = quality_df["null_count"].sum()
    total_duplicates = quality_df["duplicates"].sum()

    print(f"\nSummary:")
    print(f"  Total null values: {total_nulls}")
    print(f"  Total duplicates: {total_duplicates}")
    print(f"  Files with issues: {(quality_df['null_percentage'] > 5).sum()}")

    return {
        "quality_df": quality_df,
        "total_nulls": total_nulls,
        "total_duplicates": total_duplicates,
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = generate_quality_report()
