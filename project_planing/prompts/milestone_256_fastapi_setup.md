# Milestone #256: Set Up FastAPI Project

**Your Role:** Full-Stack Dev

Initialize FastAPI project:

```bash
pip install fastapi uvicorn[standard]
mkdir -p api
```

Create `api/main.py`:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="Shipsmart API",
    description="AI-powered logistics delay prediction",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Shipsmart API", "status": "running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

Create `requirements.txt`:
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
```

Run: `uvicorn api.main:app --reload`

Commit.