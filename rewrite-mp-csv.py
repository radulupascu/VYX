import json
import pandas as pd

def json_to_excel(json_files, csv_file, xls_file):
    all_products = []  # List to store all product dictionaries

    # Process each JSON file
    for json_file in json_files:
        with open(json_file, 'r') as file:
            data = json.load(file)
        
        # Iterate through each product
        for edge in data['data']['marketplace_search']['feed_units']['edges']:
            node = edge['node']
            listing = node['listing']
            price = listing['listing_price']['amount']  # Get raw price amount
            formatted_price = listing['listing_price']['formatted_amount']

            # Check if the currency is in RON
            if "RON" in formatted_price:
                try:
                    # Convert price to integer
                    price = int(float(price))  # Handle decimal values
                except ValueError:
                    continue  # Skip this product if the price conversion fails

                product_info = {
                    'Title': listing['marketplace_listing_title'],
                    'Price (Lei)': price,
                    'Seller': listing['marketplace_listing_seller']['name'],
                    'Location': listing['location']['reverse_geocode']['city'],
                    'Delivery_types': ', '.join(listing['delivery_types'])
                }
                all_products.append(product_info)

    # Convert list of dictionaries to DataFrame
    df = pd.DataFrame(all_products)

    # Write data to CSV
    df.to_csv(csv_file, index=False, encoding='utf-8')

    # Write data to Excel
    df.to_excel(xls_file, index=False, engine='openpyxl')

# Example usage:
json_files = [f'MarketplaceJSON/raw_response ({i}).json' for i in range(5)]
xls_file_path = 'files/marketplace-gpus.xlsx'
csv_file_path = 'files/marketplace-gpus.csv'
json_to_excel(json_files, csv_file_path, xls_file_path)
