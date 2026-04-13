# Milestone #125: Train PyTorch Neural Network (Regression)

**Your Role:** ML Engineer 2

Build PyTorch NN for regression (predict delay_minutes):
```python
class DelayRegressor(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.network = nn.Sequential(
            nn.Linear(input_dim, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1)
        )
    
    def forward(self, x):
        return self.network(x)
```

Train and save to `models/pytorch_regressor.pkl`. Evaluate RMSE, MAE, R². Commit.