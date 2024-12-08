import pandas as pd
import os
from flask import Flask, jsonify

def process_performance_tables(listings_csv_path):
    """
    Processes performance data from the listings CSV and returns categorized data.
    """
    # Load listings data
    listings_df = pd.read_csv(listings_csv_path)

    # Handle NaN values
    listings_df = listings_df.fillna({
        'views': 0,
        'num_favorers': 0,
        'favorers over views': 0
    })

    # Calculate quartiles
    views_25 = listings_df['views'].quantile(0.25)
    views_75 = listings_df['views'].quantile(0.75)

    # Add 'favorers over views' column (handling division by zero)
    listings_df['favorers over views'] = listings_df['num_favorers'] / listings_df['views'].replace(0, 1)

    # Define performance categories
    performance_categories = {
        'good_performing': listings_df[listings_df['views'] > views_75].sort_values(by='favorers over views', ascending=False).head(10),
        'under_performing': listings_df[listings_df['views'] > views_75].sort_values(by='favorers over views', ascending=True).head(10),
        'over_performing': listings_df[listings_df['views'] < views_25].sort_values(by='favorers over views', ascending=False).head(10),
        'bad_performing': listings_df[listings_df['views'] < views_25].sort_values(by='favorers over views', ascending=True).head(10)
    }

    # print(performance_categories['good_performing'].head())

    # Convert each category to dictionary format
    return {key: df.to_dict(orient='records') for key, df in performance_categories.items()}

if __name__ == '__main__':
    print(os.getcwd())
    performance_tables = process_performance_tables('app/data/listings.csv')
    print(jsonify({'performance_tables': performance_tables}))