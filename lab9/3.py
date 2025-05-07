from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix
import numpy as np

# Load customer data
customers = pd.read_csv('customers.csv')

# Clean data
customers.fillna(customers.median(), inplace=True)
customers = customers[(np.abs(customers['total_spend'] - customers['total_spend'].mean()) <= (3*customers['total_spend'].std()))]

# Feature selection
features = ['total_spend', 'age', 'visit_count', 'purchase_freq']
X = customers[features]
y = customers['high_value']

# Scale features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Split data
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Train SVM
svm_model = SVC(kernel='linear')
svm_model.fit(X_train, y_train)

# Evaluate
predictions = svm_model.predict(X_test)
print("\nCustomer Value Classification Report:")
print(classification_report(y_test, predictions))
print(f"Accuracy: {accuracy_score(y_test, predictions):.2f}")

# Decision rules
coef = svm_model.coef_[0]
intercept = svm_model.intercept_[0]
print("\nDecision Boundary Equation:")
print(f"{coef[0]:.2f}*total_spend + {coef[1]:.2f}*age + {coef[2]:.2f}*visit_count + {coef[3]:.2f}*purchase_freq + {intercept:.2f} = 0")

# Save model
joblib.dump(svm_model, 'customer_classifier.joblib')
joblib.dump(scaler, 'customer_scaler.joblib')

def classify_customer(total_spend, age, visit_count, purchase_freq):
    scaler = joblib.load('customer_scaler.joblib')
    model = joblib.load('customer_classifier.joblib')
    
    features = scaler.transform([[total_spend, age, visit_count, purchase_freq]])
    return model.predict(features)[0]
