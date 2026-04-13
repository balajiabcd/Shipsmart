# Milestone #148: Install LIME Library

**Your Role:** ML Engineer 2

Install LIME for local interpretable explanations:

```bash
pip install lime
```

Verify installation:
```python
import lime
import lime.lime_tabular
print(f"LIME version: {lime.__version__}")
```

Commit the dependency change to `requirements.txt` or `pyproject.toml`.