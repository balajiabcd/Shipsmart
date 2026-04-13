# Milestone #235: Implement Autoencoder

**Your Role:** AI/LLM Engineer

Deep learning anomaly detection:

```python
# src/anomaly/autoencoder.py

import torch
import torch.nn as nn
import pandas as pd
import numpy as np
from typing import Tuple

class Autoencoder(nn.Module):
    def __init__(self, input_dim: int, encoding_dim: int = 16):
        super().__init__()
        
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, encoding_dim)
        )
        
        self.decoder = nn.Sequential(
            nn.Linear(encoding_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 64),
            nn.ReLU(),
            nn.Linear(64, input_dim)
        )
    
    def forward(self, x):
        encoded = self.encoder(x)
        decoded = self.decoder(encoded)
        return decoded

class AutoencoderDetector:
    def __init__(self, encoding_dim: int = 16, epochs: int = 50, threshold: float = 0.1):
        self.encoding_dim = encoding_dim
        self.epochs = epochs
        self.threshold = threshold
        self.model = None
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    def fit(self, X: pd.DataFrame):
        input_dim = X.shape[1]
        self.model = Autoencoder(input_dim, self.encoding_dim).to(self.device)
        
        X_tensor = torch.FloatTensor(X.values).to(self.device)
        loader = torch.utils.data.DataLoader(X_tensor, batch_size=32, shuffle=True)
        
        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
        criterion = nn.MSELoss()
        
        for epoch in range(self.epochs):
            total_loss = 0
            for batch in loader:
                optimizer.zero_grad()
                output = self.model(batch)
                loss = criterion(output, batch)
                loss.backward()
                optimizer.step()
                total_loss += loss.item()
        
        self.model.eval()
        return self
    
    def detect(self, X: pd.DataFrame) -> np.ndarray:
        X_tensor = torch.FloatTensor(X.values).to(self.device)
        
        with torch.no_grad():
            reconstructions = self.model(X_tensor)
            mse = torch.mean((X_tensor - reconstructions) ** 2, dim=1)
        
        return (mse.cpu().numpy() > self.threshold).astype(int)
    
    def get_reconstruction_error(self, X: pd.DataFrame) -> np.ndarray:
        X_tensor = torch.FloatTensor(X.values).to(self.device)
        
        with torch.no_grad():
            reconstructions = self.model(X_tensor)
            mse = torch.mean((X_tensor - reconstructions) ** 2, dim=1)
        
        return mse.cpu().numpy()
```

Commit.