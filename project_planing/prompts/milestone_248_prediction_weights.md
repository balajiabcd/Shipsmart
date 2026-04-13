# Milestone #248: Add Weight from Delay Prediction

**Your Role:** AI/LLM Engineer

Use ML predictions for routing:

```python
# src/routing/prediction_weights.py

import joblib
import numpy as np

class PredictionWeightCalculator:
    def __init__(self, model_path: str = 'models/best_classifier.pkl'):
        self.model = joblib.load(model_path)
    
    def calculate_edge_weight(self, edge: dict, delivery_context: dict) -> float:
        base_distance = edge.get('distance_km', 10)
        
        features = self._extract_features(edge, delivery_context)
        delay_prob = self.model.predict_proba([features])[0][1]
        
        predicted_delay_mins = delay_prob * base_distance * 2
        
        traffic_factor = self._get_traffic_factor(edge.get('traffic_level', 'medium'))
        weather_factor = self._get_weather_factor(delivery_context.get('weather', 'clear'))
        
        weighted_time = base_distance * traffic_factor * weather_factor + predicted_delay_mins
        
        return weighted_time
    
    def _extract_features(self, edge: dict, context: dict) -> dict:
        return {
            'distance_km': edge.get('distance_km', 10),
            'traffic_index': {'low': 3, 'medium': 5, 'high': 8}.get(edge.get('traffic_level', 'medium'), 5),
            'weather_severity': context.get('weather_severity', 1),
            'time_of_day': context.get('hour', 12),
            'day_of_week': context.get('day_of_week', 1)
        }
    
    def _get_traffic_factor(self, traffic_level: str) -> float:
        return {'low': 1.0, 'medium': 1.5, 'high': 2.0}.get(traffic_level, 1.5)
    
    def _get_weather_factor(self, weather: str) -> float:
        return {'clear': 1.0, 'rain': 1.2, 'storm': 1.5, 'snow': 1.8}.get(weather, 1.0)
    
    def update_graph_weights(self, graph, delivery_context: dict):
        for source, edges in graph.edges.items():
            for edge in edges:
                edge.travel_time_min = self.calculate_edge_weight(edge.to_dict(), delivery_context)
```

Commit.