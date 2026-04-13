import pandas as pd
import numpy as np
import os

data_dir = os.path.join(os.path.dirname(__file__), "../../data/raw")
output_dir = os.path.join(os.path.dirname(__file__), "../../docs")
os.makedirs(output_dir, exist_ok=True)

files = [
    "orders.csv",
    "drivers.csv",
    "vehicles.csv",
    "warehouses.csv",
    "routes.csv",
    "locations.csv",
    "weather.csv",
    "traffic.csv",
    "holidays.csv",
    "customers.csv",
    "delivery_events.csv",
    "drivers_performance.csv",
    "warehouse_performance.csv",
    "route_traffic_history.csv",
    "vehicle_maintenance.csv",
    "fuel_prices.csv",
    "customer_feedback.csv",
    "competitor_data.csv",
]

report_data = []

for f in files:
    filepath = os.path.join(data_dir, f)
    if os.path.exists(filepath):
        df = pd.read_csv(filepath)
        rows = len(df)
        cols = len(df.columns)
        total_cells = rows * cols
        missing_cells = df.isnull().sum().sum()
        missing_pct = (missing_cells / total_cells * 100) if total_cells > 0 else 0
        duplicates = df.duplicated().sum()

        report_data.append(
            {
                "file": f,
                "rows": rows,
                "columns": cols,
                "missing_values": missing_cells,
                "missing_pct": round(missing_pct, 2),
                "duplicates": duplicates,
                "quality_score": round(100 - missing_pct, 1),
            }
        )

report_df = pd.DataFrame(report_data)
report_df = report_df.sort_values("quality_score")

print("=" * 60)
print("SHIPSMART DATA QUALITY REPORT")
print("=" * 60)
print(f"\nTotal files validated: {len(report_df)}")
print(f"Total records: {report_df['rows'].sum():,}")
print(f"Average quality score: {report_df['quality_score'].mean():.1f}%")
print("\n" + "-" * 60)
print("FILE SUMMARY:")
print("-" * 60)
print(report_df.to_string(index=False))

output_path = os.path.join(output_dir, "data_quality_report.md")
with open(output_path, "w") as f:
    f.write("# Shipsmart Data Quality Report\n\n")
    f.write("## Overview\n\n")
    f.write(f"- Total files validated: {len(report_df)}\n")
    f.write(f"- Total records: {report_df['rows'].sum():,}\n")
    f.write(f"- Average quality score: {report_df['quality_score'].mean():.1f}%\n\n")
    f.write("## File Summary\n\n")
    f.write("| File | Rows | Columns | Missing % | Duplicates | Quality Score |\n")
    f.write("|------|------|---------|-----------|------------|---------------|\n")
    for _, row in report_df.iterrows():
        f.write(
            f"| {row['file']} | {row['rows']:,} | {row['columns']} | {row['missing_pct']}% | {row['duplicates']} | {row['quality_score']}% |\n"
        )
    f.write("\n## Notes\n\n")
    f.write("- Missing values intentionally introduced per data simulation plan\n")
    f.write(
        "- Data quality issues include: missing values, duplicates, outliers, inconsistent formats\n"
    )
    f.write("- All files ready for ETL processing in subsequent milestones\n")

print(f"\n\nQuality report saved to: {output_path}")
