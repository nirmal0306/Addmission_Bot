import pandas as pd
from sklearn.linear_model import LinearRegression
import pickle

# Load the dataset
data = pd.read_csv("Admission_Predict.csv")  # Make sure the file is in the same directory or give full path

# Preview the column names to confirm
print("Columns in the dataset:", data.columns.tolist())

# Rename columns if necessary (depending on the CSV structure)
# Some Kaggle versions use spaces or slightly different names
data.rename(columns={
    'GRE Score': 'GRE Score',
    'TOEFL Score': 'TOEFL Score',
    'University Rating': 'University Rating',
    'SOP': 'SOP',
    'LOR ': 'LOR',
    'CGPA': 'CGPA',
    'Research': 'Research',
    'Chance of Admit ': 'Chance of Admit'  # Note the space at the end
}, inplace=True)

# Define features and target
X = data[['GRE Score', 'TOEFL Score', 'University Rating', 'SOP', 'LOR', 'CGPA', 'Research']]
y = data['Chance of Admit']

# Train the model
model = LinearRegression()
model.fit(X, y)

# Save the model
with open('admission_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model trained on CSV data and saved as 'admission_model.pkl'")
