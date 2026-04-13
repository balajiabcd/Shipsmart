# Milestone #134: Save Trained Models (ONNX)

**Your Role:** ML Engineer 2

Export models to ONNX format for interoperability:
```python
import onnx
from sklearn import sklearn2onnx
from skl2onnx.common.data_types import FloatTensorType

initial_type = [('float_input', FloatTensorType([None, X_train.shape[1]]))]
onx = sklearn2onnx.convert_sklearn(model, initial_types=initial_type)
onnx.save_model(onx, 'models/xgboost.onnx')
```

Export key models (XGBoost, LightGBM, CatBoost) to ONNX. Save to `models/*.onnx`. Commit.