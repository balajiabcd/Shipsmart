# Milestone #124: Train PyTorch Neural Network (Classification)

---

## Section 1: Instructions from Previous AI Agent

*(To be filled by Milestone #123 agent)*

---

## Section 2: Detailed Prompt to Finish Milestone

### Task: Build and Train PyTorch Neural Network for Classification

**Your Role:** ML Engineer 2

**Instructions:**
1. Create `src/ml_models/pytorch_classifier.py`:
   ```python
   import torch
   import torch.nn as nn
   import pandas as pd
   from sklearn.preprocessing import StandardScaler
   
   class DelayClassifier(nn.Module):
       def __init__(self, input_dim):
           super().__init__()
           self.network = nn.Sequential(
               nn.Linear(input_dim, 128),
               nn.ReLU(),
               nn.Dropout(0.3),
               nn.Linear(128, 64),
               nn.ReLU(),
               nn.Dropout(0.3),
               nn.Linear(64, 32),
               nn.ReLU(),
               nn.Linear(32, 1),
               nn.Sigmoid()
           )
       
       def forward(self, x):
           return self.network(x)
   
   # Prepare data
   X_train = pd.read_csv('data/ml/train_features.csv').fillna(0)
   y_train = pd.read_csv('data/ml/train_target_class.csv')['is_delayed']
   
   scaler = StandardScaler()
   X_train_scaled = scaler.fit_transform(X_train)
   
   X_tensor = torch.FloatTensor(X_train_scaled)
   y_tensor = torch.FloatTensor(y_train.values)
   
   # Train
   model = DelayClassifier(X_train.shape[1])
   criterion = nn.BCELoss()
   optimizer = torch.optim.Adam(model.parameters(), lr=0.001)
   
   for epoch in range(100):
       optimizer.zero_grad()
       outputs = model(X_tensor).squeeze()
       loss = criterion(outputs, y_tensor)
       loss.backward()
       optimizer.step()
   
   # Save
   torch.save(model.state_dict(), 'models/pytorch_classifier.pkl')
   torch.save(scaler, 'models/pytorch_scaler.pkl')
   ```

2. Evaluate and log in MLflow
3. Commit

---

## Section 3: Instructions for Next AI Agent

*(Empty)*