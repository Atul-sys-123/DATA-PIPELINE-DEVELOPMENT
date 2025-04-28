
# import pandas as pd
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split

# # Step 1: Data Ingestion
# data = pd.read_csv('data.csv')
# print("Data Loaded:")
# print(data)

# # Check data types
# print("\nData Types:")
# print(data.dtypes)

# # Step 2: Data Preprocessing
# print("\nMissing Values Before Preprocessing:")
# print(data.isnull().sum())

# # Convert 'income' to numeric, forcing errors to NaN
# data['income'] = pd.to_numeric(data['income'], errors='coerce')

# # Fill missing values (example: fill with mean for numerical columns)
# data['income'].fillna(data['income'].mean(), inplace=True)

# # Encode categorical variables (example: using one-hot encoding)
# data = pd.get_dummies(data, drop_first=True)

# print("\nData After Preprocessing:")
# print(data)

# # Step 3: Data Transformation
# X = data.drop('target', axis=1)  # Features
# y = data['target']  # Target variable

# # Scale the features
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)

# print("\nData After Scaling:")
# print(X_scaled[:5])  # Display first 5 rows of scaled data

# # Step 4: Data Loading
# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# # Save the processed data to a new CSV file
# processed_data = pd.DataFrame(X_train, columns=X.columns)
# processed_data['target'] = y_train.values  # Add the target column back
# processed_data.to_csv('processed_data.csv', index=False)

# print("\nProcessed data saved to 'processed_data.csv'")


# import pandas as pd
# from sklearn.preprocessing import StandardScaler
# from sklearn.model_selection import train_test_split

# # Step 1: Data Ingestion
# try:
#     data = pd.read_csv('data.csv')
#     print("Data Loaded Successfully. Shape:", data.shape)
#     print("\nFirst 5 rows:")
#     print(data.head())
# except FileNotFoundError:
#     raise FileNotFoundError("Error: 'data.csv' not found. Please check the file path.")

# # Check data types
# print("\nData Types:")
# print(data.dtypes)

# # Step 2: Data Preprocessing
# print("\nMissing Values Before Preprocessing:")
# print(data.isnull().sum())

# # Convert 'income' to numeric (if column exists)
# if 'income' in data.columns:
#     data['income'] = pd.to_numeric(data['income'], errors='coerce')
#     # Fill missing values with median (more robust than mean)
#     data['income'].fillna(data['income'].median(), inplace=True)
# else:
#     print("Warning: 'income' column not found in dataset")

# # Handle missing values for all numeric columns (example)
# numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
# for col in numeric_cols:
#     if data[col].isnull().any():
#         data[col].fillna(data[col].median(), inplace=True)

# # Encode categorical variables (only if they exist)
# categorical_cols = data.select_dtypes(include=['object', 'category']).columns
# if not categorical_cols.empty:
#     data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)
#     print("\nCategorical variables encoded.")
# else:
#     print("\nNo categorical variables to encode.")

# print("\nData After Preprocessing. Shape:", data.shape)
# print(data.head())

# # Step 3: Data Transformation
# # Check if 'target' column exists
# if 'target' not in data.columns:
#     raise KeyError("Error: 'target' column not found in dataset. Please check your data.")

# X = data.drop('target', axis=1)  # Features
# y = data['target']  # Target variable

# # Scale the features
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X)

# print("\nFirst 5 rows After Scaling:")
# print(X_scaled[:5])  # Display first 5 rows of scaled data

# # Step 4: Data Loading
# # Split the data into training and testing sets
# X_train, X_test, y_train, y_test = train_test_split(
#     X_scaled, y, 
#     test_size=0.2, 
#     random_state=42,
#     stratify=y  # Preserve class distribution if classification
# )

# # Save the processed data (including column names for X)
# processed_data = pd.DataFrame(X_train, columns=X.columns)
# processed_data['target'] = y_train.reset_index(drop=True)

# try:
#     processed_data.to_csv('processed_data.csv', index=False)
#     print("\nProcessed data successfully saved to 'processed_data.csv'")
# except Exception as e:
#     print(f"\nError saving file: {str(e)}")

# # Additional useful information
# print("\nTraining set shape:", X_train.shape)
# print("Test set shape:", X_test.shape)
# if y.nunique() < 10:  # Likely classification if few unique values
#     print("\nClass distribution in training set:")
#     print(y_train.value_counts(normalize=True))


import pandas as pd

try:
    data = pd.read_csv('data.csv')
    print("Data loaded successfully. Shape:", data.shape)
    print("\nFirst 5 rows:")
    print(data.head())
except FileNotFoundError:
    raise FileNotFoundError("Error: File 'data.csv' not found. Check the path or filename.")

print("\nData Types:")
print(data.dtypes)
print("\nMissing Values Before Preprocessing:")
print(data.isnull().sum())

if 'income' in data.columns:
    data['income'] = pd.to_numeric(data['income'], errors='coerce') 
    data['income'].fillna(data['income'].median(), inplace=True)  
else:
    print("Warning: 'income' column not found.")


numeric_cols = data.select_dtypes(include=['int64', 'float64']).columns
for col in numeric_cols:
    if data[col].isnull().any():
        data[col].fillna(data[col].median(), inplace=True)
    categorical_cols = data.select_dtypes(include=['object', 'category']).columns
if not categorical_cols.empty:
    data = pd.get_dummies(data, columns=categorical_cols, drop_first=True)
    print("\nCategorical variables encoded.")
else:
    print("\nNo categorical variables to encode.")

print("\nData after preprocessing. Shape:", data.shape)
print(data.head())
if 'target' not in data.columns:
    raise KeyError("Error: 'target' column not found. Check your data.")

X = data.drop('target', axis=1)
y = data['target']              
from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  

print("\nFirst 5 rows after scaling:")
print(X_scaled[:5])     
from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y,
    test_size=0.2,
    random_state=42,
    stratify=y  
)

print("\nTraining set shape:", X_train.shape)
print("Test set shape:", X_test.shape)

train_data = pd.DataFrame(X_train, columns=X.columns)
train_data['target'] = y_train.reset_index(drop=True)

try:
    train_data.to_csv('processed_data.csv', index=False)
    print("\nProcessed data saved to 'processed_data.csv'")
except Exception as e:
    print(f"Error saving file: {e}")