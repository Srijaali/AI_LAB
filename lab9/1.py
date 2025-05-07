import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt

# Load and prepare data
data = pd.read_csv('house_data.csv')
data = data.dropna()
data = pd.get_dummies(data, columns=['neighborhood'])

# Split data
X = data.drop('price', axis=1)
y = data['price']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build pipeline
numeric_features = ['square_footage', 'bedrooms', 'bathrooms', 'age']
numeric_transformer = Pipeline(steps=[
    ('scaler', StandardScaler())
])

categorical_features = [c for c in X.columns if 'neighborhood' in c]
categorical_transformer = Pipeline(steps=[
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features),
        ('cat', categorical_transformer, categorical_features)
    ])

model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
])

# Train and evaluate
model.fit(X_train, y_train)
predictions = model.predict(X_test)

print(f'RMSE: {np.sqrt(mean_squared_error(y_test, predictions)):.2f}')
print(f'R2: {r2_score(y_test, predictions):.2f}')

# Feature importance
importances = model.named_steps['regressor'].feature_importances_
features = numeric_features + list(model.named_steps['preprocessor'].named_transformers_['cat'].named_steps['onehot'].get_feature_names_out(categorical_features))
pd.DataFrame({'Feature': features, 'Importance': importances}).sort_values('Importance', ascending=False).head(10).plot.barh(x='Feature', y='Importance')
plt.show()

# Predict new house
new_house = pd.DataFrame({
    'square_footage': [1800],
    'bedrooms': [3],
    'bathrooms': [2],
    'age': [15],
    'neighborhood_Downtown': [0],
    'neighborhood_Suburban': [1],
    'neighborhood_Urban': [0]
})
print(f'Predicted price: ${model.predict(new_house)[0]:,.2f}')
