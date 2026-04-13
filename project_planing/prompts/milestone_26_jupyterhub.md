# Milestone #26: Configure Jupyter Notebooks

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #25 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Configure JupyterHub for Team

**Your Role:** DevOps Engineer

**Instructions:**
1. Install JupyterHub:
   ```bash
   pip install jupyterhub notebook
   ```

2. Create `config/jupyterhub/jupyterhub_config.py`:
   ```python
   c.JupyterHub.bind_url = 'http://0.0.0.0:8000'
   c.Authenticator.admin_user = 'admin'
   c.Spawner.default_url = '/lab'
   ```

3. Create Docker Compose for JupyterHub:
   ```yaml
   jupyterhub:
     image: jupyterhub/jupyterhub
     ports:
       - "8000:8000"
   ```

4. Create user environment setup in `docker/jupyter/Dockerfile`
5. Commit and push

---

## Section 3: Instructions for Next AI Agent

### Milestone #26 Completed
- config/jupyterhub/jupyterhub_config.py
- docker/jupyterhub-compose.yml
- docker/jupyter/Dockerfile
- Next: Milestone #27