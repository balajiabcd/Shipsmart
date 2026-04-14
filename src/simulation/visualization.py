import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import List, Dict, Optional
import io
import base64


class SimulationVisualizer:
    def __init__(self):
        self._matplotlib_available = self._check_matplotlib()

    def _check_matplotlib(self):
        try:
            import matplotlib

            return True
        except ImportError:
            return False

    def plot_delivery_timeline(
        self, history: List[Dict], save_path: Optional[str] = None
    ) -> Dict:
        if not self._matplotlib_available:
            return self._create_text_fallback(history, "timeline")

        try:
            times = [h.get("time", i) for i, h in enumerate(history)]
            active = [h.get("active_deliveries", 0) for h in history]
            completed = [h.get("completed", 0) for h in history]

            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8))

            ax1.plot(times, active, label="Active", color="blue")
            ax1.set_xlabel("Time (hours)")
            ax1.set_ylabel("Active Deliveries")
            ax1.set_title("Delivery Activity Over Time")
            ax1.legend()
            ax1.grid(True, alpha=0.3)

            ax2.bar(times, completed, color="green", alpha=0.7)
            ax2.set_xlabel("Time (hours)")
            ax2.set_ylabel("Completed Deliveries")
            ax2.set_title("Cumulative Completions")

            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=150)

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format="png", dpi=150)
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode()
            plt.close()

            return {"image": img_base64, "format": "png"}

        except Exception as e:
            return self._create_text_fallback(history, "timeline")

    def plot_scenario_comparison(
        self, results: Dict, save_path: Optional[str] = None
    ) -> Dict:
        if not self._matplotlib_available:
            return self._create_text_fallback(results, "comparison")

        try:
            scenarios = list(results.keys())
            on_time_rates = [results[s].get("on_time_rate", 0) for s in scenarios]

            fig, ax = plt.subplots(figsize=(10, 6))

            colors = ["#3498db", "#e74c3c", "#2ecc71", "#f39c12", "#9b59b6", "#95a5a6"]
            bars = ax.bar(scenarios, on_time_rates, color=colors[: len(scenarios)])

            ax.set_ylabel("On-Time Rate")
            ax.set_title("Scenario Comparison - On-Time Delivery Rate")
            ax.set_ylim(0, 1)

            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    height,
                    f"{height:.1%}",
                    ha="center",
                    va="bottom",
                )

            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=150)

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format="png", dpi=150)
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode()
            plt.close()

            return {"image": img_base64, "format": "png"}

        except Exception as e:
            return self._create_text_fallback(results, "comparison")

    def plot_weather_impact(
        self, weather_results: Dict, save_path: Optional[str] = None
    ) -> Dict:
        if not self._matplotlib_available:
            return self._create_text_fallback(weather_results, "weather")

        try:
            scenarios = list(weather_results.keys())
            delays = [
                weather_results[s].get("total_delay_minutes", 0) for s in scenarios
            ]

            fig, ax = plt.subplots(figsize=(10, 6))

            colors = ["#3498db", "#e74c3c", "#9b59b6", "#95a5a6", "#f39c12"]
            ax.bar(scenarios, delays, color=colors[: len(scenarios)])

            ax.set_ylabel("Total Delay (minutes)")
            ax.set_title("Weather Impact on Deliveries")

            plt.tight_layout()

            if save_path:
                plt.savefig(save_path, dpi=150)

            img_buffer = io.BytesIO()
            plt.savefig(img_buffer, format="png", dpi=150)
            img_buffer.seek(0)
            img_base64 = base64.b64encode(img_buffer.read()).decode()
            plt.close()

            return {"image": img_base64, "format": "png"}

        except Exception as e:
            return self._create_text_fallback(weather_results, "weather")

    def _create_text_fallback(self, data, chart_type: str) -> Dict:
        lines = [f"=== {chart_type.upper()} CHART ===", ""]

        if isinstance(data, list):
            for i, item in enumerate(data[:5]):
                lines.append(
                    f"{i + 1}. Time {item.get('time', i)}: Active={item.get('active_deliveries', 0)}"
                )
        elif isinstance(data, dict):
            for key, value in data.items():
                lines.append(f"{key}: {value}")

        return {"text": "\n".join(lines), "type": "text"}


if __name__ == "__main__":
    visualizer = SimulationVisualizer()
    print("Simulation visualizer ready")
