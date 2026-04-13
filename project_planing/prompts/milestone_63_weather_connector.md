# Milestone #63: Build Weather API Connector

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #62 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Connect to OpenWeatherMap API

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/external_apis/weather_api.py`:
   ```python
   import os
   import requests
   from datetime import datetime
   
   class WeatherAPI:
       def __init__(self):
           self.api_key = os.getenv('OPENWEATHERMAP_API_KEY')
           self.base_url = 'https://api.openweathermap.org/data/2.5'
       
       def get_current_weather(self, city):
           url = f'{self.base_url}/weather'
           params = {'q': city, 'appid': self.api_key, 'units': 'metric'}
           response = requests.get(url, params=params)
           return response.json() if response.status_code == 200 else None
       
       def get_forecast(self, city, days=5):
           url = f'{self.base_url}/forecast'
           params = {'q': city, 'appid': self.api_key, 'units': 'metric'}
           response = requests.get(url, params=params)
           return response.json() if response.status_code == 200 else None
   
   if __name__ == '__main__':
       api = WeatherAPI()
       weather = api.get_current_weather('Berlin')
       print(weather)
   ```

2. Create error handling for API failures
3. Add caching logic
4. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*