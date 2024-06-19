import pandas as pd
import re

# Path to your CSV file
file_path = 'pricy-gpus-raw.csv'

# Read the CSV file into a DataFrame
df = pd.read_csv(file_path)

# Function to clean and convert the 'Price' column
def clean_price(price):
    # Remove any non-numeric characters except for the decimal point
    price_numbers = re.findall(r'\d+\.\d+', price)
    # If found, convert the first occurrence to float and round it
    if price_numbers:
        return int(round(float(price_numbers[0])))
    # If no decimal numbers were found, try integers
    else:
        price_numbers = re.findall(r'\d+', price)
        return int(price_numbers[0]) if price_numbers else None

def clean_product_name(product_name):
    # Combine all phrases into a single pattern with the 'or' operator
    pattern = r'placa video |placa video|placă video '
    
    # Perform the replacement in a case-insensitive manner
    cleaned_name = re.sub(pattern, '', product_name, flags=re.IGNORECASE)
    
    return cleaned_name

# Apply the function to clean the 'Price' column
df['Price'] = df['Price'].apply(clean_price)
df['Product Name'] = df['Product Name'].apply(clean_product_name)

# Rename the 'Price' column to 'Price (Lei)'
df.rename(columns={'Price': 'Price (Lei)'}, inplace=True)

# Display the DataFrame to check the results
print(df)

# Write DataFrame to CSV
csv_path = "files/pricy-gpus.csv"
df.to_csv(csv_path, index=False)

# Define the path for the Excel file
excel_path = "files/pricy-gpus.xlsx"

# Write DataFrame to Excel
df.to_excel(excel_path, index=False)
