import pandas as pd
import re

data = open('olx-gpus-raw.txt').read()

def adjust_product_name(product_name, price):

    price_str = str(price)
    if len(price_str) > 4:
        product_name += price_str[:len(price_str)-4]
        price = int(price_str[-4:])
    return product_name, price

def clean_product_name(product_name):
    # Combine all phrases into a single pattern with the 'or' operator
    pattern = r'placa video |placa video|placă video |placi video |placi video|vand |vând |negociabil '
    
    # Perform the replacement in a case-insensitive manner
    cleaned_name = re.sub(pattern, '', product_name, flags=re.IGNORECASE)
    
    return cleaned_name

# Split the data into lines
lines = data.strip().split('\n')

# Define the regex pattern
pattern = re.compile(r'^(PROMOVAT ~~ )?(.*?) ~~ (\d+) lei ~~ (NEGOCIABLIL|NU) ~~ (UTILIZAT|NOU) ~~ (.*?)-')

# Parse the data
parsed_data = []
for line in lines:
    match = pattern.search(line)
    if match:
        promov = 1 if match.group(1) else 0
        product_name = match.group(2).strip()
        price = int(match.group(3))
        negociabil = 1 if match.group(4) == 'NEGOCIABLIL' else 0
        used = 1 if match.group(5) == 'UTILIZAT' else 0
        location = match.group(6).strip()
        # Adjust product name if price has more than 4 digits
        product_name = clean_product_name(product_name)
        product_name, price = adjust_product_name(product_name, price)
        
        parsed_data.append([promov, product_name, price, negociabil, used, location])

# Create DataFrame
df = pd.DataFrame(parsed_data, columns=['PROMOVAT', 'Product Name', 'Price (lei)', 'Negociabil', 'Used', 'Location'])

# Write DataFrame to CSV
csv_path = "files/olx-gpus.csv"
df.to_csv(csv_path, index=False)

# Define the path for the Excel file
excel_path = "files/olx-gpus.xlsx"

# Write DataFrame to Excel
df.to_excel(excel_path, index=False)

print(df.info())
