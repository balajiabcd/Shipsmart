# Milestone #67: Implement API Caching

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #66 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Cache API Responses

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/external_apis/cache_manager.py`:
   ```python
   import json
   import os
   import hashlib
   from datetime import datetime, timedelta
   import requests
   
   class APICache:
       def __init__(self, cache_dir='cache/', ttl_hours=1):
           self.cache_dir = cache_dir
           self.ttl = timedelta(hours=ttl_hours)
           os.makedirs(cache_dir, exist_ok=True)
       
       def _get_cache_key(self, url, params=None):
           key = url + str(params)
           return hashlib.md5(key.encode()).hexdigest()
       
       def get(self, url, params=None):
           cache_key = self._get_cache_key(url, params)
           filepath = os.path.join(self.cache_dir, f'{cache_key}.json')
           
           if os.path.exists(filepath):
               with open(filepath, 'r') as f:
                   data = json.load(f)
                   if datetime.fromisoformat(data['timestamp']) + self.ttl > datetime.now():
                       return data['response']
           return None
       
       def set(self, url, params, response):
           cache_key = self._get_cache_key(url, params)
           filepath = os.path.join(self.cache_dir, f'{cache_key}.json')
           
           with open(filepath, 'w') as f:
               json.dump({
                   'timestamp': datetime.now().isoformat(),
                   'response': response
               }, f)
   ```

2. Integrate with weather, traffic, holiday APIs
3. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*