# Milestone #28: Set Up PostgreSQL Database

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #27 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Initialize PostgreSQL Instance

**Your Role:** DevOps Engineer

**Instructions:**
1. Set up PostgreSQL via Docker:
   ```yaml
   # docker-compose.yml
   postgres:
     image: postgres:15
     environment:
       POSTGRES_DB: shipsmart
       POSTGRES_USER: shipsmart
       POSTGRES_PASSWORD: changeme
     ports:
       - "5432:5432"
     volumes:
       - postgres_data:/var/lib/postgresql/data
   ```

2. Create initialization scripts in `database/init/`
   - Schema creation script
   - Sample data loader

3. Create connection config in `config/database/config.yaml`
4. Test connection and commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*

### Milestone #28 Completed
- docker/postgres-compose.yml (PostgreSQL + pgAdmin)
- database/init/01_schema.sql (full schema)
- config/database/config.yaml
- Next: Milestone #29