# Milestone #127: Implement Early Stopping

**Your Role:** ML Engineer 2

Add early stopping to prevent overfitting:
```python
from tensorflow.keras.callbacks import EarlyStopping

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=10,
    restore_best_weights=True
)

model.fit(X_train, y_train, epochs=100, 
          validation_split=0.2,
          callbacks=[early_stop])
```

Apply to PyTorch and TensorFlow models. Commit.