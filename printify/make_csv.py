import requests
import csv
import os
from dotenv import load_dotenv
import concurrent.futures

# Load environment variables
load_dotenv()
printify_api = os.getenv("printify-api-key")

# Headers for authentication
headers = {
    'Authorization': f'Bearer {printify_api}',
    'User-Agent': 'YourAppName'
}

# Base URL for Printify API
BASE_URL = 'https://api.printify.com/v1'


# Function to get all connected shops
def get_shops():
    response = requests.get(f'{BASE_URL}/shops.json', headers=headers)
    response.raise_for_status()
    return response.json()

# For Debugging if you want to see what fields the request returns
def fetch_orders_page_fields(shop_id, page):
    response = requests.get(f'{BASE_URL}/shops/{shop_id}/orders.json?page={page}', headers=headers)
    response.raise_for_status()
    data = response.json()
    # Debug: Print the keys in the response for the first page
    if page == 1:
        print(f"Fields in the response for page {page}: {data.keys()}")
        if 'data' in data:
            print(f"Example fields in an order: {data['data'][0].keys()}")  # Show fields for one order
    return data

# Function to fetch orders for a specific page
def fetch_orders_page(shop_id, page):
    response = requests.get(f'{BASE_URL}/shops/{shop_id}/orders.json?page={page}', headers=headers)
    response.raise_for_status()
    return response.json()


# # Function to get all orders for a shop
# def get_orders(shop_id):
#     response = fetch_orders_page(shop_id, 1)
#     total_orders = response.get('data', [])
#     page = 2

#     # Fetch additional pages
#     if not total_orders:
#         return total_orders

#     with concurrent.futures.ThreadPoolExecutor() as executor:
#         future_to_page = {
#             executor.submit(fetch_orders_page, shop_id, i): i for i in range(2, 499)
#         }

#         for future in concurrent.futures.as_completed(future_to_page):
#             try:
#                 data = future.result().get('data', [])
#                 if data:
#                     total_orders.extend(data)
#                 else:
#                     break
#             except Exception as e:
#                 print(f"Error fetching page {future_to_page[future]}: {e}")

#     return total_orders

import time

def get_orders(shop_id):
    total_orders = []
    page = 1

    while True:
        try:
            response = fetch_orders_page(shop_id, page)
            data = response.get('data', [])
            if not data:  # Exit if no more data
                break

            total_orders.extend(data)
            page += 1

            # Pause after every 100 requests to prevent rate-limiting
            if page % 550 == 0:
                print("Pausing for 60 seconds to avoid rate limits...")
                time.sleep(60)  # Adjust the sleep time as needed based on the API's rate limits

        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            break

    return total_orders



def save_consolidated_orders_to_csv(all_orders):
    filename = 'all_shops_orders.csv'
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Write the header row
        writer.writerow([
            'Shop Title', 'Order ID', 'App Order ID', 'Shop ID', 'First Name', 'Last Name', 'Email',
            'Address', 'City', 'Region', 'Country', 'ZIP Code',
            'Total Price', 'Total Shipping', 'Status', 'Created At', 'Line Items', 'SKU', 'Metadata'
        ])

        for order in all_orders:

            writer.writerow([
                order['shop_title'],  # New column for shop title
                order['id'],
                order.get('app_order_id', 'N/A'),
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
                '; '.join([
                    f"{item['metadata']['title']} (Qty: {item['quantity']}, Variant: {item['metadata']['variant_label']})"
                    for item in order['line_items']
                ]),
                '; '.join([
                    f"{item['metadata']['sku']}"
                    for item in order['line_items']
                ]),
                order['metadata']  # Add the shop_order_ids as a new column
            ])

    print(f"All orders successfully written to {filename}")



# Main function to fetch and consolidate orders
def main():
    shops = get_shops()
    all_orders = []

    for shop in shops:
        shop_title = shop['title']
        print(f"Fetching orders for shop: {shop_title}")
        orders = get_orders(shop['id'])

        # Add shop title to each order
        for order in orders:
            order['shop_title'] = shop_title
        all_orders.extend(orders)

    # Save all orders to a single CSV file
    save_consolidated_orders_to_csv(all_orders)


# Run the script
if __name__ == "__main__":
    main()
    # returned = fetch_orders_page_fields(13297332 , 1)
    # print(returned)

