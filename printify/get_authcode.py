import requests
import csv

# Replace with your Printify API token
API_TOKEN = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJhdWQiOiIzN2Q0YmQzMDM1ZmUxMWU5YTgwM2FiN2VlYjNjY2M5NyIsImp0aSI6IjkxNDA0MzUwMjQ5ODljMGRmYTZhZWE0OGJiMTYzY2VlYWUxNWI3ZTExZjRhMzE4OTAzMzlhZDdiZmQ2MjNlZmU5M2ExMTYwNWVhNmY1NWMxIiwiaWF0IjoxNzMxODkxOTUzLjU4NjgyMiwibmJmIjoxNzMxODkxOTUzLjU4NjgyNiwiZXhwIjoxNzYzNDI3OTUzLjU3NjgsInN1YiI6IjE2MzIxNzc5Iiwic2NvcGVzIjpbInNob3BzLm1hbmFnZSIsInNob3BzLnJlYWQiLCJjYXRhbG9nLnJlYWQiLCJvcmRlcnMucmVhZCIsIm9yZGVycy53cml0ZSIsInByb2R1Y3RzLnJlYWQiLCJwcm9kdWN0cy53cml0ZSIsIndlYmhvb2tzLnJlYWQiLCJ3ZWJob29rcy53cml0ZSIsInVwbG9hZHMucmVhZCIsInVwbG9hZHMud3JpdGUiLCJwcmludF9wcm92aWRlcnMucmVhZCIsInVzZXIuaW5mbyJdfQ.AqIfuCOCdk8oqzK1YGSPzxWsUHbBK8uTN852osYguWxNCPqoK2HBLfwqXFrsJN-I5UKLI1AzO6QPlJLAFDU'

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

# Updated function to get all orders using parallel requests
def get_orders(shop_id):
    # Get the first page to determine if there are more pages
    response = fetch_orders_page(shop_id, 1)
    total_orders = response
    page = 2

    # If there are no more pages, return the current result
    if not response:
        return total_orders

    # Using ThreadPoolExecutor for parallel requests
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_to_page = {
            executor.submit(fetch_orders_page, shop_id, i): i for i in range(2, 20)  # Fetch up to 20 pages concurrently; adjust as needed
        }

        for future in concurrent.futures.as_completed(future_to_page):
            try:
                data = future.result()
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
def write_orders_to_csv(orders_data, sales_channel):
    # Open CSV file for writing
    filename=f'app/data/all_orders_{sales_channel}.csv'
    with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:
        writer = csv.writer(csv_file)

        # Write the header row
        writer.writerow([
            'Order ID', 'Shop ID', 'First Name', 'Last Name', 'Email',
            'Address', 'City', 'Region', 'Country', 'ZIP Code',
            'Total Price', 'Total Shipping', 'Status', 'Created At', 'Line Items'
        ])

        # Iterate over each order and write to the CSV
        for order in orders_data['data']:
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
        order_details = get_orders(shop['id'])
        write_orders_to_csv(order_details)


# Run the script
if __name__ == "__main__":
    # main()
    shops = get_shops()

    count = 0
    for shop in shops:
        if count != 0: # we don't want the first sales channel because it has nothing
            order_details = get_orders(shop['id'])
            write_orders_to_csv(order_details, shop['sales_channel'])
        count += 1
