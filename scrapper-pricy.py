from main import get_html_with_selenium
from bs4 import BeautifulSoup
import json
import time
import csv

def fetch_page(url):
    try:
        html_content = get_html_with_selenium(url)
        return html_content
    except Exception as e:
        print(f"Failed to fetch page {url}, error: {e}")
        return None

def parse_and_save(html_content, csv_writer):
    if html_content:
        soup = BeautifulSoup(html_content, 'html.parser')
        product_containers = soup.find_all('div', class_='product-container')
        for container in product_containers:
            try:
                product_info = json.loads(container.find('div', class_='product')['data-product-info'])
                product_id = product_info['id']
                product_name = product_info['name'].replace('-', ' ')
                product_price = container.find('div', class_='product-price').text.strip()
                product_image_url = container.find('img', class_='product-image')['src']

                # Write the extracted data to the CSV file
                csv_writer.writerow([product_id, product_name, product_price, product_image_url])
            except Exception as e:
                print(f"Error parsing product data: {e}")

def main():
    base_url = 'https://www.pricy.ro/products/%2Felectronice%2Faccesorii%20pentru%20electronice%2Fcomponente%20pentru%20computer%2Fpl%C4%83ci%20%C8%99i%20adaptoare%20i%2Fo%2Fpl%C4%83ci%20video%20%C8%99i%20adaptoare%20video?PageSize=20&Page={}&f_category=%2Felectronice%2Faccesorii%20pentru%20electronice%2Fcomponente%20pentru%20computer%2Fpl%C4%83ci%20%C8%99i%20adaptoare%20i%2Fo%2Fpl%C4%83ci%20video%20%C8%99i%20adaptoare%20video&min=0&max=20000'
    
    response = input("Proceed ? (y/n): ")
    if response.lower() != 'y':
        print("Exiting...")
        return

    # Open the CSV file to append
    with open('pricy-gpus-raw.csv', mode='a', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        
        # Check if the file is empty to write the header row
        file.seek(0, 2)  # Move to the end of the file
        if file.tell() == 0:
            csv_writer.writerow(['Product ID', 'Product Name', 'Price', 'Image URL'])
        
        for page_number in range(1, 501):  # Loop through 500 pages
            url = base_url.format(page_number)
            print(f"Processing page {page_number}")
            html_content = None
            for _ in range(3):  # Try up to 3 times to fetch the page
                html_content = fetch_page(url)
                if html_content:
                    break
                time.sleep(5)  # Wait for 5 seconds before retrying

            parse_and_save(html_content, csv_writer)

if __name__ == "__main__":
    main()
