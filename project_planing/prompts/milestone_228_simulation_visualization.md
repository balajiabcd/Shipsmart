# Milestone #228: Create Simulation Visualization

**Your Role:** AI/LLM Engineer

Show simulation results:

```python
# src/simulation/visualization.py

import matplotlib.pyplot as plt
import numpy as np

class SimulationVisualizer:
    def plot_delivery_timeline(self, history: list, save_path: str):
        times = [h["time"] for h in history]
        active = [h["active_deliveries"] for h in history]
        completed = [h["completed"] for h in history]
        
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
        plt.savefig(save_path, dpi=150)
        plt.close()
    
    def plot_scenario_comparison(self, results: dict, save_path: str):
        scenarios = list(results.keys())
        on_time_rates = [results[s].get("on_time_rate", 0) for s in scenarios]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        bars = ax.bar(scenarios, on_time_rates, color=["#3498db", "#e74c3c", "#2ecc71", "#f39c12"])
        
        ax.set_ylabel("On-Time Rate")
        ax.set_title("Scenario Comparison - On-Time Delivery Rate")
        ax.set_ylim(0, 1)
        
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height, f"{height:.1%}", ha='center', va='bottom')
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()
    
    def plot_weather_impact(self, weather_results: dict, save_path: str):
        scenarios = list(weather_results.keys())
        delays = [weather_results[s].get("total_delay_minutes", 0) for s in scenarios]
        
        fig, ax = plt.subplots(figsize=(10, 6))
        
        ax.bar(scenarios, delays, color=["#3498db", "#e74c3c", "#9b59b6", "#95a5a6"])
        
        ax.set_ylabel("Total Delay (minutes)")
        ax.set_title("Weather Impact on Deliveries")
        
        plt.tight_layout()
        plt.savefig(save_path, dpi=150)
        plt.close()
```

Commit.