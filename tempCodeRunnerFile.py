
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

# Step 1: Data Ingestion
data = pd.read_csv('data.csv')
print("Data Loaded:")
print(data)

# Check data types
print("\nData Types:")
print(data.dtypes)

# Step 2: Data Preprocessing
print("\nMissing Values Before Preprocessing:")
print(data.isnull().sum())

# Convert 'income' to numeric, forcing errors to NaN
data['income'] = pd.to_numeric(data['income'], errors='coerce')

# Fill missing values (example: fill with mean for numerical columns)
data['income'].fillna(data['income'].mean(), inplace=True)

# Encode categorical variables (example: using one-hot encoding)
data = pd.get_dummies(data, drop_first=True)

print("\nData After Preprocessing:")
print(data)

# Step 3: Data Transformation
X = data.drop('target', axis=1)  # Features
y = data['target']  # Target variable

# Scale the features
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

print("\nData After Scaling:")
print(X_scaled[:5])  # Display first 5 rows of scaled data

# Step 4: Data Loading
# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Save the processed data to a new CSV file
processed_data = pd.DataFrame(X_train, columns=X.columns)
processed_data['target'] = y_train.values  # Add the target column back
processed_data.to_csv('processed_data.csv', index=False)

print("\nProcessed data saved to 'processed_data.csv'")
