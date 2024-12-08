import pandas as pd
import ast


"""
This notebook aims at being able to recommend changes to Etsy product listings based on performance. 
"""

transactions_df = pd.read_csv('../data/transactions.csv')
listings_df = pd.read_csv('../data/listings.csv')

# Let's get the median number of views as a bench mark
views_25 = listings_df['views'].quantile(0.25)
views_50 = listings_df['views'].median()
views_75 = listings_df['views'].quantile(0.75)
print(views_25, views_50, views_75)

# Let's make a simpler df
listings_df['favorers over views'] = listings_df['num_favorers'] / listings_df['views']
listings2_df = listings_df[['title', 'views', 'num_favorers', 'favorers over views']]
listings2_df.sort_values(by='favorers over views', ascending=False, inplace=False).head(10)

# Good performing listings
# lot of views and good conversions
good_performing_df = listings2_df[listings2_df['views']>views_75].sort_values(by=['favorers over views'], ascending=False).head(10)
good_performing_df.head(10)

# Need to optimize price for if favorers. 

# Under performing listings
# lots of views BUT bad conversions
# => make better designs
under_performing_df = listings2_df[listings2_df['views']>views_75].sort_values(by=['favorers over views'], ascending=True).head(10)
under_performing_df.head(10)

# Over performing listings
# little views BUT good conversions
# => make better tags, keywords, quality
over_performing_df = listings2_df[listings2_df['views']<views_25].sort_values(by=['favorers over views'], ascending=False).head(10)
over_performing_df.head(10)

# Bad performing listings
# little views AND bad conversions
# => no action
bad_performing_df = listings2_df[listings2_df['views']<views_25].sort_values(by=['favorers over views'], ascending=True).head(10)
bad_performing_df.head(10)

    # Best views tags
    # get average views for each tag / total number of views
def get_best_tags(metric, listings_df):
        """
        I want to make metric for best tag performance

        Input:
        metric: metric to determine the best tag (string). column_name in listings_df.
        listings_df: listing_df

        Output:
        tag_performance_df: df with tag column and performance value column

        """
        tag_count_dict = {} # Counter for tag count
        tag_views_dict = {} # Sum of tag views 
        avg_tag_views_dict = {} # Average tags views
        for row in range(listings_df.shape[0]):
            for tag in ast.literal_eval(listings_df['tags'][row]): # basically converting from string to actual list
                if tag in tag_count_dict:
                    tag_count_dict[tag] += 1
                    tag_views_dict[tag] += listings_df[metric][row]
                else:
                    tag_count_dict[tag] = 1
                    tag_views_dict[tag] = listings_df[metric][row]
                    
                avg_tag_views_dict[tag] = tag_views_dict[tag] / tag_count_dict[tag]
        # print(tag_dict)

        # Sort the dictionary by values in descending order
        sorted_dict = dict(sorted(avg_tag_views_dict.items(), key=lambda x: x[1], reverse=True))

        # Convert to a pandas DataFrame for a tabular display
        tag_performance_df = pd.DataFrame(list(sorted_dict.items()), columns=['Tag', 'Value'])

        return tag_performance_df

best_views_tags_df = get_best_tags('views', listings_df)
best_favorers_tags_df = get_best_tags('num_favorers', listings_df)

best_views_tags_df.head()
best_favorers_tags_df.head()