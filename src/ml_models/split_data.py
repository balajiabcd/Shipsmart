import pandas as pd
import numpy as np
import os
import logging
from sklearn.model_selection import train_test_split, StratifiedKFold, TimeSeriesSplit
from typing import Tuple, Optional, Dict

logger = logging.getLogger(__name__)


def load_features_and_target(
    features_path: str = "data/raw/orders.csv", target_path: Optional[str] = None
) -> pd.DataFrame:
    """Load and merge features and target data.

    Args:
        features_path: Path to features CSV
        target_path: Path to target CSV (optional)

    Returns:
        Merged dataframe
    """
    if os.path.exists(features_path):
        df = pd.read_csv(features_path)
        logger.info(f"Loaded features: {df.shape}")
    else:
        logger.warning(f"Features file not found: {features_path}")
        df = pd.DataFrame()

    if target_path and os.path.exists(target_path):
        target_df = pd.read_csv(target_path)
        if "order_id" in df.columns and "order_id" in target_df.columns:
            df = df.merge(target_df, on="order_id", how="left")
            logger.info(f"Merged target: {target_df.shape}")

    return df


def split_data(
    df: pd.DataFrame,
    target_col: str = "is_delayed",
    regression_target_col: str = "delay_minutes",
    train_size: float = 0.7,
    val_size: float = 0.15,
    test_size: float = 0.15,
    random_state: int = 42,
    stratify: bool = True,
    id_cols: list = None,
) -> Dict[str, pd.DataFrame]:
    """Split data into train/validation/test sets.

    Args:
        df: Input dataframe
        target_col: Classification target column
        regression_target_col: Regression target column
        train_size: Train split ratio
        val_size: Validation split ratio
        test_size: Test split ratio
        random_state: Random seed
        stratify: Whether to stratify by target
        id_cols: ID columns to exclude from features

    Returns:
        Dictionary with train/val/test splits
    """
    if id_cols is None:
        id_cols = ["order_id"]

    df_clean = df.copy()

    if target_col in df_clean.columns:
        df_clean = df_clean[df_clean[target_col] != -1]

    feature_cols = [
        c
        for c in df_clean.columns
        if c not in id_cols + [target_col, regression_target_col]
    ]

    X = df_clean[feature_cols]
    y_class = df_clean[target_col] if target_col in df_clean.columns else None
    y_reg = (
        df_clean[regression_target_col]
        if regression_target_col in df_clean.columns
        else None
    )

    if stratify and y_class is not None:
        stratify_param = y_class
    else:
        stratify_param = None

    if train_size + val_size + test_size != 1.0:
        raise ValueError("Split sizes must sum to 1.0")

    X_train, X_temp, y_train, y_temp = train_test_split(
        X,
        y_class,
        test_size=(val_size + test_size),
        random_state=random_state,
        stratify=stratify_param,
    )

    val_test_ratio = val_size / (val_size + test_size)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp,
        y_temp,
        test_size=(1 - val_test_ratio),
        random_state=random_state,
        stratify=stratify_param,
    )

    result = {
        "X_train": X_train,
        "X_val": X_val,
        "X_test": X_test,
    }

    if y_class is not None:
        result["y_train_class"] = y_train
        result["y_val_class"] = y_val
        result["y_test_class"] = y_test

    if y_reg is not None:
        y_reg_train = y_reg.iloc[y_train.index]
        y_reg_val = y_reg.iloc[y_val.index]
        y_reg_test = y_reg.iloc[y_test.index]
        result["y_train_reg"] = y_reg_train
        result["y_val_reg"] = y_reg_val
        result["y_test_reg"] = y_reg_test

    return result


def save_splits(splits: Dict[str, pd.DataFrame], output_dir: str = "data/ml") -> None:
    """Save splits to CSV files.

    Args:
        splits: Dictionary of splits
        output_dir: Output directory
    """
    os.makedirs(output_dir, exist_ok=True)

    for name, df in splits.items():
        if isinstance(df, pd.DataFrame):
            filepath = os.path.join(output_dir, f"{name}.csv")
            df.to_csv(filepath, index=False)
            logger.info(f"Saved {name}: {df.shape}")


def get_split_statistics(splits: Dict[str, pd.DataFrame]) -> Dict:
    """Get statistics about the data splits.

    Args:
        splits: Dictionary of splits

    Returns:
        Statistics dictionary
    """
    stats = {}

    for name in ["X_train", "X_val", "X_test"]:
        if name in splits:
            df = splits[name]
            stats[name] = {
                "rows": len(df),
                "features": len(df.columns),
                "missing_pct": df.isnull().sum().sum()
                / (df.shape[0] * df.shape[1])
                * 100,
            }

    for suffix in ["class", "reg"]:
        for split in ["train", "val", "test"]:
            key = f"y_{split}_{suffix}"
            if key in splits:
                y = splits[key]
                if suffix == "class":
                    stats[key] = {
                        "distribution": y.value_counts().to_dict(),
                        "delay_rate": y.mean() * 100 if y is not None else 0,
                    }
                else:
                    stats[key] = {
                        "mean": y.mean() if y is not None else 0,
                        "std": y.std() if y is not None else 0,
                    }

    return stats


def create_time_series_split(
    df: pd.DataFrame,
    date_col: str = "order_time",
    target_col: str = "is_delayed",
    n_splits: int = 5,
) -> TimeSeriesSplit:
    """Create time series cross-validation splits.

    Args:
        df: Input dataframe
        date_col: Date column for sorting
        target_col: Target column
        n_splits: Number of splits

    Returns:
        TimeSeriesSplit object
    """
    if date_col in df.columns:
        df = df.sort_values(date_col)

    return TimeSeriesSplit(n_splits=n_splits)


def create_stratified_kfold(
    n_splits: int = 5, shuffle: bool = True, random_state: int = 42
) -> StratifiedKFold:
    """Create stratified k-fold cross-validation.

    Args:
        n_splits: Number of folds
        shuffle: Whether to shuffle
        random_state: Random seed

    Returns:
        StratifiedKFold object
    """
    return StratifiedKFold(
        n_splits=n_splits, shuffle=shuffle, random_state=random_state
    )


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    try:
        df = pd.read_csv("data/raw/orders.csv")
        splits = split_data(df, train_size=0.7, val_size=0.15, test_size=0.15)
        save_splits(splits)

        stats = get_split_statistics(splits)
        print("\n=== Split Statistics ===")
        for key, val in stats.items():
            print(f"{key}: {val}")

    except Exception as e:
        logger.error(f"Error: {e}")
        print(f"Creating sample split data for demonstration...")

        X = pd.DataFrame(
            {
                "feature1": np.random.randn(1000),
                "feature2": np.random.randn(1000),
                "feature3": np.random.randint(0, 5, 1000),
            }
        )
        y_class = np.random.randint(0, 2, 1000)
        y_reg = np.random.randn(1000)

        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y_class, test_size=0.3, random_state=42
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, random_state=42
        )

        splits = {
            "X_train": X_train,
            "X_val": X_val,
            "X_test": X_test,
            "y_train_class": pd.Series(y_train),
            "y_val_class": pd.Series(y_val),
            "y_test_class": pd.Series(y_test),
        }
        save_splits(splits)
        print("Sample split data saved!")
