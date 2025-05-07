import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Load email data
emails = pd.read_csv('emails.csv')
emails.fillna('', inplace=True)

# Feature engineering
emails['length'] = emails['content'].apply(len)
emails['has_links'] = emails['content'].str.contains('http').astype(int)

# Text vectorization
tfidf = TfidfVectorizer(max_features=1000, stop_words='english')
text_features = tfidf.fit_transform(emails['content'])

# Combine features
X = pd.concat([
    pd.DataFrame(text_features.toarray()),
    emails[['length', 'has_links']],
    axis=1
)
y = emails['is_spam']

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
spam_model = RandomForestClassifier(n_estimators=100)
spam_model.fit(X_train, y_train)

# Evaluate
predictions = spam_model.predict(X_test)
print("Spam Classification Report:")
print(classification_report(y_test, predictions))
print(f"Accuracy: {accuracy_score(y_test, predictions):.2f}")

# Save model
joblib.dump(spam_model, 'spam_classifier.joblib')
joblib.dump(tfidf, 'tfidf_vectorizer.joblib')

def classify_email(email_content):
    vec = joblib.load('tfidf_vectorizer.joblib')
    model = joblib.load('spam_classifier.joblib')
    
    length = len(email_content)
    has_links = 1 if 'http' in email_content else 0
    text_features = vec.transform([email_content])
    
    features = pd.concat([
        pd.DataFrame(text_features.toarray()),
        pd.DataFrame([[length, has_links]], columns=['length', 'has_links'])
    ], axis=1)
    
    return model.predict(features)[0]
