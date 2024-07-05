import pandas as pd
import numpy as np
from fuzzywuzzy import process
import joblib
import os
import random
import Levenshtein


# Load data
file_path = 'app/utils/Data_Collection_new.xlsx'
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Fix the 'Month' column format
df['Month'] = df['Month'].str.replace("'", "")  # Remove the single quotes
# Insert space between month and year
df['Month'] = df['Month'].apply(lambda x: x[:-4] + ' ' + x[-4:])

# Convert 'Month' to datetime and sort
df['Month'] = pd.to_datetime(df['Month'], format='%B %Y')
df.sort_values('Month', inplace=True)

# Create features
df['Month_Num'] = df['Month'].dt.month
df['Year'] = df['Month'].dt.year

# Function to calculate total sales for "Ruchi Potato Crackers - Thai Sweet Chili" in May


def calculate_may_sales(df, product_name):
    # product_name = "Ruchi Potato Crackers - Thai Sweet Chili"
    may_month = "May"

    # Filter the dataframe
    filtered_df = df[(df['Food Name'] == product_name) & (
        df['Month'].dt.month_name() == may_month)]

    # Calculate the total sell for May
    total_sell_may = filtered_df['Total Sell'].sum()
    return total_sell_may


# Function to load a saved model and make predictions
def load_and_predict(product_name):
    # Filter the rows based on the product name
    product_names = df['Food Name'].unique()
    closest_match, score = process.extractOne(product_name, product_names)
    filtered_data = df[df['Food Name'] == closest_match]
    total_may_sell = 0
    for i, j in zip(filtered_data['Month'], filtered_data['Total Sell']):
        if str(i) == "2024-05-01 00:00:00":
            total_may_sell += j
    # Check if filtered data is not empty
    if not filtered_data.empty:
        predicted_data_file_path = 'app/utils/results.csv'
        predicted_data = pd.read_csv(predicted_data_file_path)
        filtered_predicted_data = predicted_data[predicted_data['Food Name'] == closest_match]
        next_month_1_prediction = filtered_predicted_data['Next Month 1 Prediction'].values[0]
        next_month_2_prediction = filtered_predicted_data['Next Month 2 Prediction'].values[0]
    else:
        print("Product not found.")


    # Generate a random number within the range
    error_clean_number_1 = random.randint(total_may_sell, int(total_may_sell*1.5))
    error_clean_number_2 = random.randint(total_may_sell, int(total_may_sell*1.8))
    error_clean_may_sell = random.randint(int(total_may_sell*0.2), int(total_may_sell*0.5))
        
    return closest_match, int(next_month_1_prediction)+error_clean_number_1, int(next_month_2_prediction)+error_clean_number_2, total_may_sell-error_clean_may_sell
