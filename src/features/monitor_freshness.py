import pandas as pd
import numpy as np
import os
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


FRESHNESS_THRESHOLDS = {
    "temporal_features.csv": 24,
    "distance_features.csv": 168,
    "weather_features.csv": 1,
    "traffic_features.csv": 0.5,
    "driver_scores.csv": 24,
    "warehouse_scores.csv": 24,
    "route_complexity.csv": 168,
    "seasonality_features.csv": 24,
    "holiday_features.csv": 24,
    "weather_location.csv": 1,
    "target.csv": 24,
}


def check_feature_freshness(features_dir: str = "data/features") -> pd.DataFrame:
    """Check and report feature freshness.

    Args:
        features_dir: Directory containing feature CSV files

    Returns:
        DataFrame with freshness report
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
            row_count = len(df)
            file_mtime = datetime.fromtimestamp(os.path.getmtime(filepath))
            file_age_hours = (datetime.now() - file_mtime).total_seconds() / 3600

            timestamp_cols = [
                c
                for c in df.columns
                if any(t in c.lower() for t in ["time", "date", "timestamp"])
            ]

            if timestamp_cols:
                try:
                    latest_ts = pd.to_datetime(
                        df[timestamp_cols[0]], errors="coerce"
                    ).max()
                    if pd.notna(latest_ts):
                        data_age_hours = (
                            datetime.now() - latest_ts
                        ).total_seconds() / 3600
                    else:
                        data_age_hours = file_age_hours
                except:
                    data_age_hours = file_age_hours
            else:
                data_age_hours = file_age_hours

            threshold = FRESHNESS_THRESHOLDS.get(filename, 24)
            is_fresh = data_age_hours <= threshold

            results.append(
                {
                    "feature_file": filename,
                    "row_count": row_count,
                    "file_age_hours": round(file_age_hours, 2),
                    "data_age_hours": round(data_age_hours, 2),
                    "threshold_hours": threshold,
                    "is_fresh": is_fresh,
                    "last_checked": datetime.now().isoformat(),
                }
            )

        except Exception as e:
            logger.error(f"Error checking {filename}: {e}")
            results.append(
                {
                    "feature_file": filename,
                    "row_count": 0,
                    "file_age_hours": -1,
                    "data_age_hours": -1,
                    "threshold_hours": FRESHNESS_THRESHOLDS.get(filename, 24),
                    "is_fresh": False,
                    "last_checked": datetime.now().isoformat(),
                    "error": str(e),
                }
            )

    return pd.DataFrame(results)


def get_stale_features(freshness_df: pd.DataFrame) -> List[str]:
    """Get list of stale feature files."""
    return freshness_df[~freshness_df["is_fresh"]]["feature_file"].tolist()


def generate_freshness_alert(freshness_df: pd.DataFrame) -> Dict:
    """Generate alert for stale features."""
    stale = get_stale_features(freshness_df)

    if stale:
        return {
            "alert": True,
            "severity": "high" if len(stale) > 3 else "medium",
            "stale_features": stale,
            "message": f"{len(stale)} feature(s) are stale: {', '.join(stale)}",
        }

    return {
        "alert": False,
        "severity": "none",
        "stale_features": [],
        "message": "All features are fresh",
    }


def save_freshness_report(
    freshness_df: pd.DataFrame, output_path: str = "data/features/freshness_report.csv"
):
    """Save freshness report to CSV."""
    freshness_df.to_csv(output_path, index=False)
    logger.info(f"Saved freshness report to {output_path}")


def run_freshness_check() -> Dict:
    """Run full freshness check and return results."""
    freshness_df = check_feature_freshness()

    if not freshness_df.empty:
        save_freshness_report(freshness_df)
        alert = generate_freshness_alert(freshness_df)

        print("\n=== Feature Freshness Report ===")
        print(freshness_df.to_string(index=False))
        print(f"\nAlert: {alert['message']}")

        return {"freshness_df": freshness_df, "alert": alert}

    return {
        "freshness_df": freshness_df,
        "alert": {"alert": False, "message": "No features found"},
    }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    result = run_freshness_check()
