# Milestone #218: Create Visual Explanations

**Your Role:** AI/LLM Engineer

Generate explanation visualizations:

```python
# src/root_cause/visualizations.py

import matplotlib.pyplot as plt
import numpy as np

class ExplanationVisualizer:
    def __init__(self):
        self.colors = {"positive": "#e74c3c", "negative": "#27ae60", "neutral": "#95a5a6"}
    
    def create_waterfall_chart(self, shap_values, prediction, save_path: str):
        features = [s["feature"] for s in shap_values[:8]]
        values = [s["shap_value"] for s in shap_values[:8]]
        
        base_value = 0.5
        cumulative = [base_value]
        
        for v in values:
            cumulative.append(cumulative[-1] + v)
        
        fig, ax = plt.subplots(figsize=(12, 6))
        
        ax.barh(features, values, color=[self.colors["positive"] if v > 0 else self.colors["negative"] for v in values])
        ax.axvline(x=0, color="black", linewidth=0.5)
        
        ax.set_xlabel("Impact on Delay Probability")
        ax.set_title(f"Delay Explanation - Prediction: {prediction:.1%}")
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()
    
    def create_factor_importance_chart(self, shap_values, save_path: str):
        sorted_vals = sorted(shap_values, key=lambda x: abs(x["shap_value"]), reverse=True)[:10]
        
        features = [s["feature"] for s in sorted_vals]
        abs_values = [abs(s["shap_value"]) for s in sorted_vals]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.barh(features[::-1], abs_values[::-1], color=self.colors["neutral"])
        
        ax.set_xlabel("Absolute SHAP Value")
        ax.set_title("Top Delay Factors")
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()
    
    def create_confidence_gauge(self, confidence_score: float, save_path: str):
        fig, ax = plt.subplots(figsize=(6, 4), subplot_kw={"projection": "polar"})
        
        theta = np.linspace(0, np.pi, 100)
        ax.fill_between(theta, 0.5, 1, color=self.colors["neutral"], alpha=0.3)
        
        needle_angle = np.pi * (1 - confidence_score)
        ax.plot([0, 0.8 * np.cos(needle_angle)], [0, 0.8 * np.sin(needle_angle)], "k-", lw=3)
        
        ax.set_title(f"Confidence: {confidence_score:.0%}")
        ax.axis("off")
        
        plt.savefig(save_path, dpi=150)
        plt.close()
```

Commit.