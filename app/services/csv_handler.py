import pandas as pd
import os
from flask import Flask, jsonify
import math
import ast
 
def convert_nan_to_null(data):
    if isinstance(data, dict):  # If the data is a dictionary
        return {key: convert_nan_to_null(value) for key, value in data.items()}
    elif isinstance(data, list):  # If the data is a list
        return [convert_nan_to_null(item) for item in data]
    elif isinstance(data, float) and math.isnan(data):  # If the value is NaN
        return None
    else:
        return data
    
def get_best_tags(metric, listings_df):
    """
    Calculate the performance of tags based on the given metric.
    
    Args:
        metric (str): The column name representing the metric (e.g., 'views', 'favorers').
        listings_df (pd.DataFrame): DataFrame containing the listings data. 
                                    Must include 'tags' column (list-like) and the metric column.

    Returns:
        pd.DataFrame: DataFrame with tags and their average performance score.
    """
    # Ensure 'tags' column is properly formatted as lists
    listings_df['tags'] = listings_df['tags'].apply(lambda x: ast.literal_eval(x) if isinstance(x, str) else x)
    
    # Explode the 'tags' column to simplify processing
    exploded_df = listings_df.explode('tags')
    
    # Group by tag and calculate metrics
    tag_group = exploded_df.groupby('tags')[metric].agg(['sum', 'count'])
    tag_group['average_score'] = tag_group['sum'] / tag_group['count']
    
    # Sort tags by their performance scores
    sorted_tags = tag_group[['average_score']].sort_values(by='average_score', ascending=False).reset_index()
    
    return sorted_tags.rename(columns={'tags': 'Tag', 'average_score': 'Score'})

# Example usage:
# result = get_best_tags('views', listings_df)

def process_performance_tables(listings_csv_path, transactions_csv_path):
    # def process_performance_tables(listings_csv_path):
    """
    Processes performance data from the listings CSV and returns categorized data.
    """
    # Load listings data
    listings_df = pd.read_csv(listings_csv_path)

    transactions_df = pd.read_csv(transactions_csv_path)

    print('listings')
    # print(listings_df.columns)
    print('transactions')
    # print(transactions_df.columns)

    num_sales = transactions_df.groupby('listing_id').size().reset_index(name='num_sales')

    print('num_sales')
    # print(num_sales.head())

    listings_df = listings_df.merge(num_sales, on='listing_id', how='left')

    print('listings')
    # print(listings_df.head())

    # Handle NaN values in num_sales
    listings_df['num_sales'] = listings_df['num_sales'].fillna(0).astype(int)

    # Handle NaN values
    listings_df = listings_df.fillna(0)

    # Calculate quartiles
    views_25 = listings_df['views'].quantile(0.25)
    views_75 = listings_df['views'].quantile(0.75)

    # Get the median views
    best_views_tags_df = get_best_tags('views', listings_df)
    median_view_score = best_views_tags_df['Score'].median()

    # Add 'favorers over views' column (handling division by zero)
    listings_df['favorers_over_views'] = round(((listings_df['num_favorers'] / listings_df['views'].replace(0, 1))*100),1)

    listings_df['conversion_rate'] = round(((listings_df['num_sales'] / listings_df['views'].replace(0, 1)) * 100),1)
    
    # Create a dictionary for quick lookup of tag scores
    tag_scores = best_views_tags_df.set_index('Tag')['Score'].to_dict()

    # Create the tags_to_change column
    def find_tags_to_change(tags):
        """Identify tags with scores below the median view score."""
        return [tag for tag in tags if tag_scores.get(tag, 0) < median_view_score]
    
    def find_tags_to_keep(tags):
        """Identify tags with scores below the median view score."""
        return [tag for tag in tags if tag_scores.get(tag, 0) >= median_view_score]

    listings_df['tags_to_change'] = listings_df['tags'].apply(find_tags_to_change)
    listings_df['tags_to_keep'] = listings_df['tags'].apply(find_tags_to_keep)

    print(listings_df['tags_to_change'].head())

    # Define performance categories
    performance_categories = {
        'good_performing': listings_df[listings_df['views'] > views_75].sort_values(by='favorers_over_views', ascending=False).head(100),
        'under_performing': listings_df[listings_df['views'] > views_75].sort_values(by='favorers_over_views', ascending=True).head(100),
        'over_performing': listings_df[listings_df['views'] < views_25].sort_values(by='favorers_over_views', ascending=False).head(100),
        'bad_performing': listings_df[listings_df['views'] < views_25].sort_values(by='favorers_over_views', ascending=True).head(100)
    }

    # print(performance_categories['good_performing'].head())

    # Convert each category to dictionary format
    return {key: df.to_dict(orient='records') for key, df in performance_categories.items()}

if __name__ == '__main__':
    print(os.getcwd())
    listings_csv_path = 'app/data/listings.csv'
    transactions_csv_path = 'app/data/transactions.csv'

    performance_tables = process_performance_tables(listings_csv_path, transactions_csv_path)