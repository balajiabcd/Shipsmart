# Milestone #14: Generate Customers CSV (Unclean)

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #13 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Generate customers.csv with PII Issues

**Your Role:** Data Engineer

**Instructions:**
1. Create `src/data_simulation/generate_customers.py`
2. Generate 20,000 customer records: customer_id, name, email, phone, address, city, registration_date
3. **Issues:** Real PII-like data (needs anonymization reminder), 2% duplicate emails
4. Output: `data/raw/customers.csv`
5. Commit and push

**Note:** Add a comment that PII should be handled according to GDPR in production.

---

## Section 3: Instructions for Next AI Agent

### Milestone #14 Completed
- customers.csv (20K), generate_customers.py
- 2% duplicate emails, 3% missing phone
- NOTE: Handle PII according to GDPR
- Next: Milestone #15