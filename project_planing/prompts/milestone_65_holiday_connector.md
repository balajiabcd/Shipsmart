# Milestone #65: Build Holiday API Connector

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #64 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Connect to Nager.Date Holiday API

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/external_apis/holiday_api.py`:
   ```python
   import requests
   
   class HolidayAPI:
       BASE_URL = 'https://date.nager.at/api/v3'
       
       def get_holidays(self, year, country='DE'):
           url = f'{self.BASE_URL}/PublicHolidays/{year}/{country}'
           response = requests.get(url)
           return response.json() if response.status_code == 200 else []
       
       def get_next_holidays(self, country='DE', days=30):
           from datetime import datetime, timedelta
           # Get upcoming holidays
           pass
   ```

2. Test for German holidays
3. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*