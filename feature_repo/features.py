from feast import Field
from feast.feature_view import FeatureView
from feast.feature import Feature
from feast.data_source import FileSource
from feast.value_type import Int64, Float, String, Bool
from datetime import timedelta

order_df = FileSource(
    path="data/features/temporal_features.csv",
    timestamp_field="order_id",
    created_timestamp_column="created_at",
)

temporal_fv = FeatureView(
    name="temporal_features",
    entities=["order_id"],
    ttl=timedelta(days=1),
    features=[
        Field(name="hour", dtype=Int64),
        Field(name="day_of_week", dtype=Int64),
        Field(name="month", dtype=Int64),
        Field(name="quarter", dtype=Int64),
        Field(name="is_weekend", dtype=Int64),
        Field(name="is_business_hour", dtype=Int64),
    ],
    online=True,
    batch_source=order_df,
)

distance_fv = FeatureView(
    name="distance_features",
    entities=["order_id"],
    ttl=timedelta(days=7),
    features=[
        Field(name="distance_km", dtype=Float),
        Field(name="distance_bucket", dtype=String),
        Field(name="is_long_distance", dtype=Int64),
    ],
    online=True,
    batch_source=FileSource(
        path="data/features/distance_features.csv",
        timestamp_field="order_id",
    ),
)

weather_fv = FeatureView(
    name="weather_features",
    entities=["location_id"],
    ttl=timedelta(hours=1),
    features=[
        Field(name="weather_severity_index", dtype=Float),
        Field(name="is_bad_weather", dtype=Int64),
        Field(name="temp_severity", dtype=Int64),
    ],
    online=True,
    batch_source=FileSource(
        path="data/features/weather_features.csv",
        timestamp_field="location_id",
    ),
)

driver_fv = FeatureView(
    name="driver_features",
    entities=["driver_id"],
    ttl=timedelta(days=1),
    features=[
        Field(name="performance_score", dtype=Float),
        Field(name="on_time_rate", dtype=Float),
        Field(name="is_top_performer", dtype=Int64),
    ],
    online=True,
    batch_source=FileSource(
        path="data/features/driver_scores.csv",
        timestamp_field="driver_id",
    ),
)

warehouse_fv = FeatureView(
    name="warehouse_features",
    entities=["warehouse_id"],
    ttl=timedelta(days=1),
    features=[
        Field(name="efficiency_score", dtype=Float),
        Field(name="is_bottleneck", dtype=Int64),
    ],
    online=True,
    batch_source=FileSource(
        path="data/features/warehouse_scores.csv",
        timestamp_field="warehouse_id",
    ),
)

traffic_fv = FeatureView(
    name="traffic_features",
    entities=["route_id"],
    ttl=timedelta(minutes=30),
    features=[
        Field(name="traffic_index", dtype=Float),
        Field(name="is_peak_hour", dtype=Int64),
    ],
    online=True,
    batch_source=FileSource(
        path="data/features/traffic_features.csv",
        timestamp_field="route_id",
    ),
)

route_fv = FeatureView(
    name="route_features",
    entities=["route_id"],
    ttl=timedelta(days=7),
    features=[
        Field(name="route_complexity_index", dtype=Float),
        Field(name="is_complex_route", dtype=Int64),
    ],
    online=True,
    batch_source=FileSource(
        path="data/features/route_complexity.csv",
        timestamp_field="route_id",
    ),
)

holiday_fv = FeatureView(
    name="holiday_features",
    entities=["order_id"],
    ttl=timedelta(days=1),
    features=[
        Field(name="is_holiday", dtype=Int64),
        Field(name="is_holiday_week", dtype=Int64),
    ],
    online=True,
    batch_source=FileSource(
        path="data/features/holiday_features.csv",
        timestamp_field="order_id",
    ),
)


def register_features():
    from feast import FeatureStore

    fs = FeatureStore(repo_path="feature_repo")
    fs.apply(
        [
            temporal_fv,
            distance_fv,
            weather_fv,
            driver_fv,
            warehouse_fv,
            traffic_fv,
            route_fv,
            holiday_fv,
        ]
    )
    print("Features registered successfully!")


if __name__ == "__main__":
    print("Feast feature definitions created.")
    print("To apply: cd feature_repo && feast apply")
