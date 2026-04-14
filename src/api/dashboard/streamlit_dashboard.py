import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json

st.set_page_config(
    page_title="Shipsmart Dashboard",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE = "http://localhost:8000/api/v1"

st.markdown(
    """
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1e3a8a;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8fafc;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #3b82f6;
    }
    .stAlert {
        padding: 0.5rem;
    }
</style>
""",
    unsafe_allow_html=True,
)


def check_api_health():
    try:
        response = requests.get(f"{API_BASE}/health", timeout=2)
        return response.status_code == 200
    except:
        return False


def get_predictions(order_ids=None):
    if not order_ids:
        order_ids = [f"ORD-{i:05d}" for i in range(1, 6)]
    return order_ids


def get_alerts(severity=None):
    try:
        response = requests.get(
            f"{API_BASE}/alerts",
            params={"severity": severity} if severity else {},
            timeout=5,
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return {
        "alerts": [
            {
                "alert_id": "ALERT-001",
                "severity": "high",
                "message": "Munich region: 35% increase in delays",
                "timestamp": datetime.now().isoformat(),
            },
            {
                "alert_id": "ALERT-002",
                "severity": "medium",
                "message": "Heavy rain in Berlin region",
                "timestamp": datetime.now().isoformat(),
            },
        ],
        "count": 2,
        "high_severity_count": 1,
    }


def predict_delivery(
    order_id, origin_lat, origin_lon, dest_lat, dest_lon, scheduled_date, scheduled_time
):
    try:
        response = requests.post(
            f"{API_BASE}/predict",
            json={
                "order_id": order_id,
                "origin_lat": origin_lat,
                "origin_lon": origin_lon,
                "destination_lat": dest_lat,
                "destination_lon": dest_lon,
                "scheduled_date": scheduled_date,
                "scheduled_time": scheduled_time,
            },
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        st.error(f"API Error: {e}")
    return None


def get_recommendations(order_id, delay_probability):
    try:
        response = requests.post(
            f"{API_BASE}/recommend",
            json={"order_id": order_id, "delay_probability": delay_probability},
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None


def get_route_optimization(origin, destination):
    try:
        response = requests.post(
            f"{API_BASE}/route/optimize",
            json={
                "origin": {
                    "id": origin["id"],
                    "lat": origin["lat"],
                    "lon": origin["lon"],
                },
                "destination": {
                    "id": destination["id"],
                    "lat": destination["lat"],
                    "lon": destination["lon"],
                },
                "optimization_type": "distance",
            },
            timeout=10,
        )
        if response.status_code == 200:
            return response.json()
    except:
        pass
    return None


def main():
    st.markdown(
        '<div class="main-header">🚚 Shipsmart Dashboard</div>', unsafe_allow_html=True
    )

    with st.sidebar:
        st.header("Navigation")
        page = st.radio(
            "Go to",
            ["Overview", "Predictions", "Alerts", "Routes", "Simulation", "Settings"],
        )

        st.divider()

        st.subheader("API Status")
        if check_api_health():
            st.success("✅ API Connected")
        else:
            st.warning("⚠️ API Offline - Using Demo Mode")

    if page == "Overview":
        overview_page()
    elif page == "Predictions":
        predictions_page()
    elif page == "Alerts":
        alerts_page()
    elif page == "Routes":
        routes_page()
    elif page == "Simulation":
        simulation_page()
    elif page == "Settings":
        settings_page()


def overview_page():
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Total Deliveries", "1,234", "+12%")
    with col2:
        st.metric("On-Time Rate", "87%", "+2%")
    with col3:
        st.metric("Active Drivers", "45", "+5")
    with col4:
        st.metric("Active Alerts", "2", "-1")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Delay Trends")
        dates = pd.date_range(start=datetime.now() - timedelta(days=7), periods=7)
        delays = [12, 18, 15, 22, 19, 14, 16]
        df = pd.DataFrame({"Date": dates, "Delays": delays})
        fig = px.line(df, x="Date", y="Delays", markers=True)
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Alerts by Severity")
        alert_data = {"High": 1, "Medium": 4, "Low": 2}
        fig = px.pie(
            values=list(alert_data.values()), names=list(alert_data.keys()), hole=0.4
        )
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("Recent Predictions")
    with st.expander("View Recent Predictions", expanded=True):
        pred_data = []
        for i in range(1, 6):
            result = predict_delivery(
                f"ORD-{i:05d}",
                52.52,
                13.405,
                48.13,
                11.58,
                datetime.now().strftime("%Y-%m-%d"),
                "14:00",
            )
            if result:
                pred_data.append(result)
            else:
                pred_data.append(
                    {
                        "order_id": f"ORD-{i:05d}",
                        "predicted_delay": i % 2 == 0,
                        "delay_probability": 0.5 + (i * 0.1),
                        "confidence": "medium",
                        "model_version": "xgboost_v1.0",
                    }
                )

        df = pd.DataFrame(pred_data)
        st.dataframe(df, use_container_width=True)


def predictions_page():
    st.header("🎯 Delay Predictions")

    col1, col2 = st.columns([1, 2])

    with col1:
        st.subheader("Make a Prediction")
        with st.form("prediction_form"):
            order_id = st.text_input("Order ID", "ORD-00001")
            origin_lat = st.number_input("Origin Latitude", value=52.52)
            origin_lon = st.number_input("Origin Longitude", value=13.405)
            dest_lat = st.number_input("Destination Latitude", value=48.13)
            dest_lon = st.number_input("Destination Longitude", value=11.58)
            scheduled_date = st.date_input("Scheduled Date", datetime.now())
            scheduled_time = st.time_input(
                "Scheduled Time", datetime.strptime("14:00", "%H:%M")
            )

            submitted = st.form_submit_button("Predict", type="primary")

        if submitted:
            result = predict_delivery(
                order_id,
                origin_lat,
                origin_lon,
                dest_lat,
                dest_lon,
                str(scheduled_date),
                scheduled_date.strftime("%H:%M"),
            )

            if result:
                st.session_state["prediction_result"] = result

    with col2:
        st.subheader("Prediction Result")
        if "prediction_result" in st.session_state:
            result = st.session_state["prediction_result"]

            col_a, col_b = st.columns(2)
            with col_a:
                st.metric("Delay Probability", f"{result['delay_probability']:.1%}")
            with col_b:
                st.metric(
                    "Prediction", "Delayed" if result["predicted_delay"] else "On-Time"
                )

            st.info(f"Confidence: {result['confidence']}")
            st.caption(f"Model Version: {result['model_version']}")

            recs = get_recommendations(order_id, result["delay_probability"])
            if recs and recs.get("recommendations"):
                st.subheader("Recommendations")
                for rec in recs["recommendations"]:
                    with st.expander(f"{rec['action']} - {rec['priority']}"):
                        st.write(rec["description"])
                        st.caption(f"Impact: {rec['estimated_impact']}")
        else:
            st.info("Enter prediction parameters and click Predict")

    st.divider()
    st.subheader("Batch Predictions")

    if st.button("Run Batch Prediction"):
        results = []
        for i in range(1, 11):
            result = predict_delivery(
                f"ORD-{i:05d}",
                52.52,
                13.405,
                48.13 + (i * 0.1),
                11.58 + (i * 0.1),
                datetime.now().strftime("%Y-%m-%d"),
                "14:00",
            )
            if not result:
                result = {
                    "order_id": f"ORD-{i:05d}",
                    "predicted_delay": i % 3 == 0,
                    "delay_probability": 0.3 + (i * 0.05),
                    "confidence": "medium",
                    "model_version": "xgboost_v1.0",
                }
            results.append(result)

        df = pd.DataFrame(results)
        st.dataframe(df, use_container_width=True)

        delayed_count = sum(1 for r in results if r["predicted_delay"])
        st.metric("Predicted Delays", f"{delayed_count}/{len(results)}")


def alerts_page():
    st.header("🔔 Anomaly Alerts")

    col1, col2, col3 = st.columns(3)

    alerts_data = get_alerts()

    with col1:
        st.metric("Total Alerts", alerts_data.get("count", 0))
    with col2:
        st.metric("High Severity", alerts_data.get("high_severity_count", 0))
    with col3:
        st.metric("Active", alerts_data.get("count", 0) - 10)

    st.subheader("Recent Alerts")

    for alert in alerts_data.get("alerts", []):
        severity_color = {"high": "error", "medium": "warning", "low": "info"}.get(
            alert.get("severity"), "info"
        )

        with st.expander(f"{alert['alert_id']} - {alert['severity'].upper()}"):
            st.write(alert["message"])
            st.caption(f"Timestamp: {alert.get('timestamp', 'N/A')}")

            if st.button(f"Acknowledge {alert['alert_id']}", key=alert["alert_id"]):
                st.success(f"Alert {alert['alert_id']} acknowledged")


def routes_page():
    st.header("🗺️ Route Optimization")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Origin")
        origin_id = st.text_input("Origin ID", "depot")
        origin_lat = st.number_input("Origin Latitude", value=52.52)
        origin_lon = st.number_input("Origin Longitude", value=13.405)

    with col2:
        st.subheader("Destination")
        dest_id = st.text_input("Destination ID", "munich")
        dest_lat = st.number_input("Destination Latitude", value=48.13)
        dest_lon = st.number_input("Destination Longitude", value=11.58)

    if st.button("Optimize Route", type="primary"):
        result = get_route_optimization(
            {"id": origin_id, "lat": origin_lat, "lon": origin_lon},
            {"id": dest_id, "lat": dest_lat, "lon": dest_lon},
        )

        if result:
            st.success(f"Route found: {' → '.join(result.get('path', []))}")

            col1, col2 = st.columns(2)
            col1.metric("Total Distance", f"{result.get('total_distance', 0):.1f} km")
            col2.metric("Total Time", f"{result.get('total_time', 0):.1f} min")
        else:
            st.info("Route: Berlin → Munich (simulated)")
            col1, col2 = st.columns(2)
            col1.metric("Total Distance", "584 km")
            col2.metric("Total Time", "345 min")

    st.divider()
    st.subheader("Multi-Route Optimization")

    with st.expander("Configure Multi-Route"):
        num_vehicles = st.slider("Number of Vehicles", 2, 5, 3)
        st.write(
            "This would optimize routes for multiple deliveries across specified vehicles"
        )


def simulation_page():
    st.header("🔬 Scenario Simulation")

    scenario_type = st.selectbox(
        "Scenario Type",
        ["demand", "driver_shortage", "weather", "fuel", "warehouse", "competitor"],
    )

    col1, col2 = st.columns(2)

    with col1:
        duration = st.slider("Duration (hours)", 1, 72, 24)
        num_deliveries = st.number_input("Number of Deliveries", 10, 1000, 100)

    with col2:
        if scenario_type == "demand":
            multiplier = st.slider("Demand Multiplier", 0.5, 2.0, 1.0)
        elif scenario_type == "driver_shortage":
            shortage = st.slider("Shortage %", 0.0, 0.5, 0.2)
        elif scenario_type == "weather":
            weather = st.selectbox(
                "Weather Condition", ["rain", "snow", "fog", "clear"]
            )
        else:
            st.write("Configure additional parameters")

    if st.button("Run Simulation", type="primary"):
        st.info(f"Running {scenario_type} simulation...")

        mock_results = {
            "demand": {
                "expected_delays": int(num_deliveries * 0.12 * multiplier),
                "avg_delay_duration": 18 * multiplier,
                "driver_utilization": 85 * multiplier,
                "warehouse_load": 72 * multiplier,
            },
            "driver_shortage": {
                "expected_delays": int(num_deliveries * 0.18),
                "avg_delay_duration": 22,
                "driver_utilization": 92,
                "warehouse_load": 75,
            },
            "weather": {
                "expected_delays": int(num_deliveries * 0.15),
                "avg_delay_duration": 25,
                "driver_utilization": 78,
                "warehouse_load": 70,
            },
        }

        results = mock_results.get(
            scenario_type,
            {
                "expected_delays": int(num_deliveries * 0.12),
                "avg_delay_duration": 18,
                "driver_utilization": 85,
                "warehouse_load": 72,
            },
        )

        st.subheader("Simulation Results")

        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric("Expected Delays", results["expected_delays"])
            st.metric("Avg Delay Duration", f"{results['avg_delay_duration']:.0f} min")
        with res_col2:
            st.metric("Driver Utilization", f"{results['driver_utilization']:.0f}%")
            st.metric("Warehouse Load", f"{results['warehouse_load']:.0f}%")


def settings_page():
    st.header("⚙️ Settings")

    st.subheader("API Configuration")

    api_url = st.text_input("API Base URL", API_BASE)
    st.caption(f"Currently pointing to: {api_url}")

    st.subheader("Model Settings")

    model_version = st.selectbox(
        "Model Version", ["xgboost_v1.0", "random_forest_v1.0", "lightgbm_v1.0"]
    )

    st.subheader("LLM Configuration")

    llm_provider = st.selectbox(
        "LLM Provider", ["Ollama (Local)", "OpenAI (Cloud)", "Anthropic (Cloud)"]
    )

    if llm_provider == "Ollama (Local)":
        ollama_model = st.selectbox("Model", ["phi3", "llama3:8b", "mistral"])
        st.caption("Using local Ollama instance for privacy")

    st.divider()

    if st.button("Save Settings", type="primary"):
        st.success("Settings saved successfully!")


if __name__ == "__main__":
    main()
