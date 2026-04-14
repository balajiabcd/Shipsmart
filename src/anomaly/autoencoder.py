import pandas as pd
import numpy as np
from typing import Tuple, Optional


class AutoencoderDetector:
    def __init__(
        self, encoding_dim: int = 16, epochs: int = 50, threshold: float = 0.1
    ):
        self.encoding_dim = encoding_dim
        self.epochs = epochs
        self.threshold = threshold
        self.model = None
        self.is_fitted = False
        self._torch_available = self._check_torch()

    def _check_torch(self):
        try:
            import torch

            return True
        except ImportError:
            return False

    def _create_model(self, input_dim: int):
        if not self._torch_available:
            return None

        try:
            import torch
            import torch.nn as nn

            class Autoencoder(nn.Module):
                def __init__(self, input_dim, encoding_dim):
                    super().__init__()
                    self.encoder = nn.Sequential(
                        nn.Linear(input_dim, 64),
                        nn.ReLU(),
                        nn.Linear(64, 32),
                        nn.ReLU(),
                        nn.Linear(32, encoding_dim),
                    )
                    self.decoder = nn.Sequential(
                        nn.Linear(encoding_dim, 32),
                        nn.ReLU(),
                        nn.Linear(32, 64),
                        nn.ReLU(),
                        nn.Linear(64, input_dim),
                    )

                def forward(self, x):
                    return self.decoder(self.encoder(x))

            return Autoencoder(input_dim, self.encoding_dim)
        except:
            return None

    def fit(self, X: pd.DataFrame):
        if not self._torch_available:
            self.is_fitted = False
            return self

        try:
            import torch
            import torch.nn as nn

            input_dim = X.shape[1]
            self.model = self._create_model(input_dim)

            if self.model is None:
                self.is_fitted = False
                return self

            device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
            self.model = self.model.to(device)

            X_tensor = torch.FloatTensor(X.values).to(device)
            loader = torch.utils.data.DataLoader(X_tensor, batch_size=32, shuffle=True)

            optimizer = torch.optim.Adam(self.model.parameters(), lr=0.001)
            criterion = nn.MSELoss()

            for epoch in range(self.epochs):
                self.model.train()
                for batch in loader:
                    optimizer.zero_grad()
                    output = self.model(batch)
                    loss = criterion(output, batch)
                    loss.backward()
                    optimizer.step()

            self.model.eval()
            self.is_fitted = True

        except Exception as e:
            self.is_fitted = False

        return self

    def detect(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted or self.model is None:
            return np.zeros(len(X))

        try:
            import torch

            device = next(self.model.parameters()).device
            X_tensor = torch.FloatTensor(X.values).to(device)

            with torch.no_grad():
                reconstructions = self.model(X_tensor)
                mse = torch.mean((X_tensor - reconstructions) ** 2, dim=1)

            return (mse.cpu().numpy() > self.threshold).astype(int)
        except:
            return np.zeros(len(X))

    def get_reconstruction_error(self, X: pd.DataFrame) -> np.ndarray:
        if not self.is_fitted or self.model is None:
            return np.zeros(len(X))

        try:
            import torch

            device = next(self.model.parameters()).device
            X_tensor = torch.FloatTensor(X.values).to(device)

            with torch.no_grad():
                reconstructions = self.model(X_tensor)
                mse = torch.mean((X_tensor - reconstructions) ** 2, dim=1)

            return mse.cpu().numpy()
        except:
            return np.zeros(len(X))

    def fit_detect(self, X: pd.DataFrame) -> pd.Series:
        self.fit(X)
        predictions = self.detect(X)
        return pd.Series(predictions, index=X.index)


if __name__ == "__main__":
    detector = AutoencoderDetector()
    print("Autoencoder detector ready")
