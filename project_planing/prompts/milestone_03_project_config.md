# Milestone #3: Create Project Configuration

---

## Section 1: Instructions from Previous AI Agent

**From Milestone #2:**
- venv created with all core packages
- requirements.txt populated
- Python environment verified

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Create Project Configuration Files

**Project Context:**
- Project: Shipsmart
- **GitHub Repository:** https://github.com/balajiabcd/Shipsmart

**Your Role:**
You are a **Full-Stack Developer** creating configuration files.

**Instructions:**

1. **Create config.yaml**
   Create `config.yaml` with:
   ```yaml
   project:
     name: shipsmart
     tagline: "The Brain Behind Every Delivery."
     version: 1.0.0
     environment: development
   
   data:
     raw_dir: ./data/raw
     processed_dir: ./data/processed
     features_dir: ./data/features
   
   database:
     postgres:
       host: localhost
       port: 5432
       database: shipsmart
       user: shipsmart
       password: changeme
   
   api:
     host: 0.0.0.0
     port: 8000
     reload: true
   
   ml:
     experiment_tracking:
       provider: mlflow
       tracking_uri: http://localhost:5000
   
   kubernetes:
     namespace: shipsmart
     ingress_class: nginx
   ```

2. **Create .env.example**
   Copy from existing template with all API keys, database credentials, etc.

3. **Create pyproject.toml** (optional)
   For Python package management

4. **Create setup scripts**
   - `scripts/setup.sh` - Linux/Mac setup
   - `scripts/setup.bat` - Windows setup

5. **Update README.md**
   Add installation and setup instructions.

6. **Commit and Push**
   ```bash
   git add .
   git commit -m "Add project configuration files"
   git push
   ```

**Subagent Task:**
If needed, ask DevOps Engineer for Kubernetes configuration best practices.

---

## Section 3: Instructions for Next AI Agent

### Milestone Completion Summary

**Completed Tasks:**
1. ✅ Created pyproject.toml with project metadata
2. ✅ Created scripts/setup.bat (Windows)
3. ✅ Created scripts/setup.sh (Linux/Mac)
4. ✅ Created Makefile with common commands
5. ✅ config.yaml already existed (comprehensive)
6. ✅ .env.example already existed
7. ✅ Pushed to GitHub

**Files Created:**
- `pyproject.toml` - Python project metadata
- `scripts/setup.bat` - Windows setup script
- `scripts/setup.sh` - Linux/Mac setup script
- `Makefile` - Common commands

**Git Status:**
- Branch: main
- Last commit: "Milestone #3: Add project configuration files"

**Project Status:**
- Configuration complete
- Ready for Milestone #4: Data Plan

### Instructions for Next AI Agent (Milestone #4)

Proceed to: `project_planing/prompts/milestone_04_data_plan.md`