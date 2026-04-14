import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Optional
import io
import base64


class ExplanationVisualizer:
    def __init__(self):
        self.colors = {
            "positive": "#e74c3c",
            "negative": "#27ae60",
            "neutral": "#95a5a6",
        }
        self._matplotlib_available = self._check_matplotlib()

    def _check_matplotlib(self):
        try:
            import matplotlib

            return True
        except ImportError:
            return False

    def create_waterfall_chart(
        self,
        shap_values: List[Dict],
        prediction: float,
        save_path: Optional[str] = None,
    ):
        if not self._matplotlib_available:
            return self._create_text_fallback(shap_values, prediction, "waterfall")

        try:
            features = [s["feature"] for s in shap_values[:8]]
            values = [s.get("shap_value", 0) for s in shap_values[:8]]

            base_value = 0.5
            cumulative = [base_value]
            for v in values:
                cumulative.append(cumulative[-1] + v)

            fig, ax = plt.subplots(figsize=(12, 6))

            colors = [
                self.colors["positive"] if v > 0 else self.colors["negative"]
                for v in values
            ]
            ax.barh(features, values, color=colors)
            ax.axvline(x=0, color="black", linewidth=0.5)

            ax.set_xlabel("Impact on Delay Probability")
            ax.set_title(f"Delay Explanation - Prediction: {prediction:.1%}")

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
            return self._create_text_fallback(shap_values, prediction, "waterfall")

    def create_factor_importance_chart(
        self, shap_values: List[Dict], save_path: Optional[str] = None
    ):
        if not self._matplotlib_available:
            return self._create_text_fallback(shap_values, 0, "importance")

        try:
            sorted_vals = sorted(
                shap_values, key=lambda x: abs(x.get("shap_value", 0)), reverse=True
            )[:10]

            features = [s["feature"] for s in sorted_vals]
            abs_values = [abs(s.get("shap_value", 0)) for s in sorted_vals]

            fig, ax = plt.subplots(figsize=(10, 6))
            ax.barh(features[::-1], abs_values[::-1], color=self.colors["neutral"])

            ax.set_xlabel("Absolute SHAP Value")
            ax.set_title("Top Delay Factors")

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
            return self._create_text_fallback(shap_values, 0, "importance")

    def create_confidence_gauge(
        self, confidence_score: float, save_path: Optional[str] = None
    ):
        if not self._matplotlib_available:
            return {"text": f"Confidence: {confidence_score:.0%}", "type": "text"}

        try:
            fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={"projection": "polar"})

            theta = np.linspace(0, np.pi, 100)
            ax.fill_between(theta, 0.5, 1, color=self.colors["neutral"], alpha=0.3)

            needle_angle = np.pi * (1 - confidence_score)
            ax.plot(
                [0, 0.8 * np.cos(needle_angle)],
                [0, 0.8 * np.sin(needle_angle)],
                "k-",
                lw=3,
            )

            ax.set_title(f"Confidence: {confidence_score:.0%}")
            ax.axis("off")

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
            return {"text": f"Confidence: {confidence_score:.0%}", "type": "text"}

    def _create_text_fallback(
        self, shap_values: List[Dict], prediction: float, chart_type: str
    ) -> dict:
        lines = [
            f"=== {chart_type.upper()} CHART ===",
            f"Prediction: {prediction:.1%}",
            "",
        ]

        for i, s in enumerate(shap_values[:8]):
            direction = "↑" if s.get("shap_value", 0) > 0 else "↓"
            lines.append(
                f"{i + 1}. {s['feature']}: {direction} {abs(s.get('shap_value', 0)):.3f}"
            )

        return {"text": "\n".join(lines), "type": "text"}


if __name__ == "__main__":
    visualizer = ExplanationVisualizer()
    result = visualizer.create_factor_importance_chart(
        [
            {"feature": "weather", "shap_value": 0.45},
            {"feature": "traffic", "shap_value": 0.32},
        ]
    )
    print("Visualizer ready")
