import pandas as pd
import os
from flask import Flask, jsonify
import math
 
def convert_nan_to_null(data):
    if isinstance(data, dict):  # If the data is a dictionary
        return {key: convert_nan_to_null(value) for key, value in data.items()}
    elif isinstance(data, list):  # If the data is a list
        return [convert_nan_to_null(item) for item in data]
    elif isinstance(data, float) and math.isnan(data):  # If the value is NaN
        return None
    else:
        return data
def process_performance_tables(listings_csv_path, transactions_csv_path):
    # def process_performance_tables(listings_csv_path):
    """
    Processes performance data from the listings CSV and returns categorized data.
    """
    # Load listings data
    listings_df = pd.read_csv(listings_csv_path)

    transactions_df = pd.read_csv(transactions_csv_path)

    print('listings')
    print(listings_df.columns)
    print('transactions')
    print(transactions_df.columns)

    num_sales = transactions_df.groupby('listing_id').size().reset_index(name='num_sales')

    print('num_sales')
    print(num_sales.head())

    listings_df = listings_df.merge(num_sales, on='listing_id', how='left')

    print('listings')
    print(listings_df.head())

    # Handle NaN values in num_sales
    listings_df['num_sales'] = listings_df['num_sales'].fillna(0).astype(int)

    # Handle NaN values
    listings_df = listings_df.fillna(0)

    # Calculate quartiles
    views_25 = listings_df['views'].quantile(0.25)
    views_75 = listings_df['views'].quantile(0.75)

    # Add 'favorers over views' column (handling division by zero)
    listings_df['favorers_over_views'] = listings_df['num_favorers'] / listings_df['views'].replace(0, 1)

    listings_df['conversion_rate'] = round(((listings_df['num_sales'] / listings_df['views'].replace(0, 1)) * 100),1)

    # Define performance categories
    performance_categories = {
        'good_performing': listings_df[listings_df['views'] > views_75].sort_values(by='favorers_over_views', ascending=False).head(10),
        'under_performing': listings_df[listings_df['views'] > views_75].sort_values(by='favorers_over_views', ascending=True).head(10),
        'over_performing': listings_df[listings_df['views'] < views_25].sort_values(by='favorers_over_views', ascending=False).head(10),
        'bad_performing': listings_df[listings_df['views'] < views_25].sort_values(by='favorers_over_views', ascending=True).head(10)
    }

    # print(performance_categories['good_performing'].head())

    # Convert each category to dictionary format
    return {key: df.to_dict(orient='records') for key, df in performance_categories.items()}

if __name__ == '__main__':
    print(os.getcwd())
    listings_csv_path = 'app/data/listings.csv'
    transactions_csv_path = 'app/data/transactions.csv'

    performance_tables = process_performance_tables(listings_csv_path, transactions_csv_path)
    # print(performance_tables['good_performing'])