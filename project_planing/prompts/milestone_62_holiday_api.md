# Milestone #62: Register Holiday API (Nager.Date)

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #61 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Get Nager.Date Holiday API Access

**Your Role:** Data Engineer

**Instructions:**
1. Go to https://date.nager.at/
2. API is free, no registration needed for basic use
3. Test endpoint:
   ```python
   import requests
   url = 'https://date.nager.at/api/v3/PublicHolidays/2026/DE'
   response = requests.get(url)
   print(response.json())
   ```
4. Add to `.env.example`: `NAGER_DATE_BASE_URL=https://date.nager.at/api/v3`
5. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*