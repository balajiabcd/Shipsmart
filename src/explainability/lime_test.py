import lime
import lime.lime_tabular
import numpy as np

print("LIME installed successfully!")

X = np.random.rand(100, 5)
explainer = lime.lime_tabular.LimeTabularExplainer(X, mode="classification")
print("LIME explainer created successfully!")
