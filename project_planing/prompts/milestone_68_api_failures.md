# Milestone #68: Handle API Failures

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #67 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Add Retry Logic to API Calls

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/external_apis/retry_handler.py`:
   ```python
   import time
   import requests
   from functools import wraps
   
   def retry_on_failure(max_retries=3, backoff_factor=2):
       def decorator(func):
           @wraps(func)
           def wrapper(*args, **kwargs):
               for attempt in range(max_retries):
                   try:
                       return func(*args, **kwargs)
                   except (requests.exceptions.RequestException, 
                            requests.exceptions.Timeout) as e:
                       if attempt == max_retries - 1:
                           raise e
                       wait_time = backoff_factor ** attempt
                       print(f"Attempt {attempt+1} failed, retrying in {wait_time}s...")
                       time.sleep(wait_time)
               return None
           return wrapper
       return decorator
   
   class RobustAPI:
       @retry_on_failure(max_retries=3, backoff_factor=2)
       def fetch_with_retry(self, url, **kwargs):
           response = requests.get(url, timeout=10, **kwargs)
           response.raise_for_status()
           return response.json()
   ```

2. Apply retry decorator to all API connectors
3. Add logging for failed requests
4. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*