# Milestone #64: Build Traffic API Connector

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #63 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Connect to TomTom/HERE Traffic API

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/external_apis/traffic_api.py`:
   ```python
   import os
   import requests
   
   class TrafficAPI:
       def __init__(self):
           self.tomtom_key = os.getenv('TOMTOM_API_KEY')
           self.here_key = os.getenv('HERE_API_KEY')
       
       def get_traffic_flow(self, lat, lon):
           # TomTom example
           url = f'https://api.tomtom.com/traffic/services/4/flowSegmentData/absolute/10/{lat},{lon}?key={self.tomtom_key}'
           response = requests.get(url)
           return response.json() if response.status_code == 200 else None
       
       def get_route_traffic(self, origin, destination):
           # HERE example
           url = f'https://router.hereapi.com/v8/routes'
           params = {
               'origin': origin,
               'destination': destination,
               'transportMode': 'car',
               'apiKey': self.here_key
           }
           response = requests.get(url, params=params)
           return response.json() if response.status_code == 200 else None
   ```

2. Handle API errors gracefully
3. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*