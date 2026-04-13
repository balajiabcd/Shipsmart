# Milestone #66: Create API Rate Limiter

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #65 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Handle API Rate Limits

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/external_apis/rate_limiter.py`:
   ```python
   import time
   from collections import defaultdict
   from threading import Lock
   
   class RateLimiter:
       def __init__(self, calls_per_minute=60):
           self.calls_per_minute = calls_per_minute
           self.calls = defaultdict(list)
           self.lock = Lock()
       
       def acquire(self, key='default'):
           with self.lock:
               now = time.time()
               # Remove calls older than 1 minute
               self.calls[key] = [t for t in self.calls[key] if now - t < 60]
               
               if len(self.calls[key]) >= self.calls_per_minute:
                   return False
               
               self.calls[key].append(now)
               return True
       
       def wait_if_needed(self, key='default'):
           while not self.acquire(key):
               time.sleep(1)
   ```

2. Integrate with all API connectors
3. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*