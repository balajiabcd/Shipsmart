# Milestone #131: Train CNN Model

**Your Role:** ML Engineer 2

Build 1D CNN for spatial feature patterns:
```python
class CNN1DClassifier(nn.Module):
    def __init__(self, input_dim):
        super().__init__()
        self.conv1 = nn.Conv1d(input_dim, 64, kernel_size=3, padding=1)
        self.pool = nn.MaxPool1d(2)
        self.conv2 = nn.Conv1d(64, 32, kernel_size=3, padding=1)
        self.fc = nn.Linear(32, 1)
        self.sigmoid = nn.Sigmoid()
```

Note: Requires reshaping input to (batch, channels, features). Save to `models/cnn_classifier.pkl`. Commit.