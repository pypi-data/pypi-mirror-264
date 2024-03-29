import joblib

# Assuming your model file is named 'model.pkl'
xgb_model = joblib.load('model.pkl')

__all__ = ['xgb_model']

