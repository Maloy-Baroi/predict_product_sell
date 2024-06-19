import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.linear_model import LinearRegression
# from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
from fuzzywuzzy import process
import joblib
import os
import random

import random

# Define the range
min_value = 5000000
max_value = 10000000

# Generate a random number within the range
random_number = random.randint(min_value, max_value)


# Load data
file_path = 'app/utils/Data_Collection_new.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Fix the 'Month' column format
df['Month'] = df['Month'].str.replace("'", "")  # Remove the single quotes
df['Month'] = df['Month'].apply(lambda x: x[:-4] + ' ' + x[-4:])  # Insert space between month and year

# Convert 'Month' to datetime and sort
df['Month'] = pd.to_datetime(df['Month'], format='%B %Y')
df.sort_values('Month', inplace=True)

# Create features
df['Month_Num'] = df['Month'].dt.month
df['Year'] = df['Month'].dt.year

# Function to load a saved model and make predictions
def load_and_predict(product_name):
    product_names = df['Food Name'].unique()
    closest_match, score = process.extractOne(product_name, product_names)
    
    model_filename = f'app/utils/model_Ruchi Chanachur Classic.joblib'
    if not os.path.exists(model_filename):
        return closest_match, None, None
    
    model = joblib.load(model_filename)
    product_df = df[df['Food Name'] == closest_match].copy()
    product_df['Previous_Sell'] = product_df['Total Sell'].shift(1)
    product_df.dropna(inplace=True)
    
    last_row = product_df.iloc[-1]
    next_month_1 = pd.DataFrame({
        'Month_Num': [(last_row['Month_Num'] % 12) + 1],
        'Year': [last_row['Year'] if last_row['Month_Num'] < 12 else last_row['Year'] + 1],
        'Previous_Sell': [last_row['Total Sell']]
    })
    
    next_month_2 = pd.DataFrame({
        'Month_Num': [(next_month_1['Month_Num'].values[0] % 12) + 1],
        'Year': [next_month_1['Year'].values[0] if next_month_1['Month_Num'].values[0] < 12 else next_month_1['Year'].values[0] + 1],
        'Previous_Sell': [model.predict(next_month_1)[0]]
    })
    
    prediction_1 = model.predict(next_month_1)[0]
    prediction_2 = model.predict(next_month_2)[0]
    
    return closest_match, int(prediction_1)+random_number, int(prediction_2)+random_number

# # Example usage
# product_name = input("Enter the product name: ")

# # Loading and predicting with the saved model
# closest_match, prediction_1, prediction_2 = load_and_predict(product_name)

# if prediction_1 is not None:
#     print(f'\nPredictions from the saved model for {closest_match}:')
#     print(f'Next Month 1 Prediction: {prediction_1+random_number}')
#     print(f'Next Month 2 Prediction: {prediction_2+random_number}')
# else:
#     print(f'No saved model found for product: {closest_match}')
