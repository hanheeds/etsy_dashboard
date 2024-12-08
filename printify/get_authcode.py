import requests
import csv

import os
from dotenv import load_dotenv


load_dotenv() 
printify_api = os.getenv("printify-api-key")

# Replace with your Printify API token
API_TOKEN = printify_api

# Headers for authentication
headers = {
    'Authorization': f'Bearer {API_TOKEN}',
    'User-Agent': 'YourAppName'
}

# Base URL for Printify API
BASE_URL = 'https://api.printify.com/v1'

# Function to get all connected shops
def get_shops():
    response = requests.get(f'{BASE_URL}/shops.json', headers=headers)
    response.raise_for_status()
    return response.json()

import requests
import concurrent.futures

# Function to fetch orders for a specific page
def fetch_orders_page(shop_id, page):
    response = requests.get(f'{BASE_URL}/shops/{shop_id}/orders.json?page={page}', headers=headers)
    response.raise_for_status()
    return response.json()

# Get the total number of pages
def get_total_pages(shop_id):
    response = fetch_orders_page(shop_id, 1)
    total_records = response.get('total', 0)
    per_page = len(response.get('data', []))  # Number of records per page

    if per_page > 0:
        total_pages = (total_records // per_page) + (1 if total_records % per_page != 0 else 0)
    else:
        total_pages = 1

    return total_pages

# Updated function to get all orders using parallel requests
def get_orders(shop_id):
    # Get the first page to determine if there are more pages
    response = fetch_orders_page(shop_id, 1)
    total_orders = response.get('data',[])
    # total_pages = get_total_pages(shop_id)
    page = 2

    # If there are no more pages, return the current result
    if not total_orders:
        return total_orders

    # Using ThreadPoolExecutor for parallel requests
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_page = {
            executor.submit(fetch_orders_page, shop_id, i): i for i in range(2, 499)  # Fetch up to 20 pages concurrently; adjust as needed
        }

        for future in concurrent.futures.as_completed(future_to_page):
            try:
                data = future.result().get('data',[])
                if data:
                    total_orders.extend(data)
                else:
                    break  # No more data
            except Exception as e:
                print(f'Error fetching page {future_to_page[future]}: {e}')

    return total_orders

# Function to save order data to a CSV file
def save_orders_to_csv(shop_title, orders):
    filename = f'{shop_title}_orders.csv'
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Write header row
        writer.writerow(['Order ID', 'Status', 'Total Price', 'Line Items'])

        for order in orders:
            line_items = '; '.join([f"{item['title']} (Qty: {item['quantity']})" for item in order['line_items']])
            writer.writerow([order['id'], order['status'], order['total_price'], line_items])
    
    print(f'Data for {shop_title} saved to {filename}')

import csv

# Function to write all orders to a single CSV file
def write_orders_to_csv(orders_data, sales_channel, shop_title):
    # Open CSV file for writing
    filename=f'app/data/all_orders_{sales_channel}_{shop_title}.csv'
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Write the header row
        writer.writerow([
            'Order ID', 'Shop ID', 'First Name', 'Last Name', 'Email',
            'Address', 'City', 'Region', 'Country', 'ZIP Code',
            'Total Price', 'Total Shipping', 'Status', 'Created At', 'Line Items'
        ])

        # Iterate over each order and write to the CSV
        for order in orders_data:
            line_items = '; '.join([
                f"{item['metadata']['title']} (Qty: {item['quantity']}, Variant: {item['metadata']['variant_label']})"
                for item in order['line_items']
            ])
            writer.writerow([
                order['id'],
                order['shop_id'],
                order['address_to']['first_name'],
                order['address_to']['last_name'],
                order['address_to']['email'],
                f"{order['address_to']['address1']} {order['address_to']['address2']}".strip(),
                order['address_to']['city'],
                order['address_to']['region'],
                order['address_to']['country'],
                order['address_to']['zip'],
                order['total_price'],
                order['total_shipping'],
                order['status'],
                order['created_at'],
                line_items
            ])

    print(f"Orders successfully written to {filename}")

# Example usage with your data
orders_data = {
    'data': [
        # Add your order data here as shown in the sample JSON structure
    ],
    'current_page': 1,
    'total': 928
}


# Main function to get shops and their orders, and save them as CSV files
def main():
    shops = get_shops()
    for shop in shops:
        print(shop['title'])
        print('total pages: ')
        print(get_total_pages(shop['id']))
        order_details = get_orders(shop['id'])
        write_orders_to_csv(order_details, shop['sales_channel'], shop['title'])

# Run the script
if __name__ == "__main__":
    main()