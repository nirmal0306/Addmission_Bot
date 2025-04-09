import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Sample data
data = pd.DataFrame({
    'GRE Score': [320, 315, 310, 305, 300],
    'TOEFL Score': [110, 105, 102, 99, 95],
    'University Rating': [5, 4, 3, 3, 2],
    'SOP': [4.5, 4.0, 3.5, 3.0, 2.5],
    'LOR': [4.5, 4.0, 3.5, 3.0, 2.5],
    'CGPA': [9.0, 8.5, 8.0, 7.5, 7.0],
    'Research': [1, 1, 0, 0, 0],
    'Chance of Admit': [0.9, 0.85, 0.78, 0.72, 0.65]
})

# Define features and target
X = data[['GRE Score', 'TOEFL Score', 'University Rating', 'SOP', 'LOR', 'CGPA', 'Research']]
y = data['Chance of Admit']

# Train the model
model = LinearRegression()
model.fit(X, y)

# Save the model to a file
with open('admission_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("✅ Model trained and saved as 'admission_model.pkl'")
