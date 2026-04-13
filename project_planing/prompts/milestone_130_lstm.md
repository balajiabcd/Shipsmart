# Milestone #130: Train LSTM Model

**Your Role:** ML Engineer 2

Build LSTM for time-series data:
```python
import torch.nn as nn

class LSTMClassifier(nn.Module):
    def __init__(self, input_dim, hidden_dim=64):
        super().__init__()
        self.lstm = nn.LSTM(input_dim, hidden_dim, batch_first=True)
        self.fc = nn.Linear(hidden_dim, 1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x):
        lstm_out, _ = self.lstm(x.unsqueeze(1))
        out = self.fc(lstm_out[:, -1, :])
        return self.sigmoid(out)
```

Note: Requires sequence data - may need to create sequences from temporal features. Save to `models/lstm_classifier.pkl`. Commit.