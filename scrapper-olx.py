from main import get_html_with_selenium, parse_and_replace, add_newline_after_phrase, separate_product_price, add_newline_after_date, correct_year_price, remove_first_and_last_line
import time
from bs4 import BeautifulSoup

products_path = 'olx-gpus-raw.txt'

# Iterate through 25 pages
for page_number in range(1, 25):
    print(f"Scraping page {page_number}...")
    url = f'https://www.olx.ro/electronice-si-electrocasnice/componente-laptop-pc/placi-video/?currency=RON&page={page_number}'
    retries = 10
    for attempt in range(retries):
        try:
            html_content = get_html_with_selenium(url)
            soup = BeautifulSoup(html_content, 'html.parser')

            # Extracting all text within <div> tags
            div_texts = [div.get_text(strip=True) for div in soup.find_all('div')]

            # Parse and process the text
            parsed_text = parse_and_replace(div_texts[1])
            parsed_text = add_newline_after_phrase(parsed_text)
            parsed_text = separate_product_price(parsed_text)
            parsed_text = add_newline_after_date(parsed_text)
            parsed_text = correct_year_price(parsed_text)
            parsed_text = remove_first_and_last_line(parsed_text)

            # Append the parsed text to the file
            with open(products_path, 'a', encoding='utf-8') as file:
                file.write(parsed_text + '\n')
            
            break  # Exit the retry loop if successful
        except Exception as e:
            print(f"Failed to retrieve page {page_number}, attempt {attempt + 1}. Retrying...")
            time.sleep(5)  # Wait before retrying
            if attempt == retries - 1:
                print(f"Failed to retrieve page {page_number} after {retries} attempts.")

print(f"Scraping complete. Products have been written to {products_path}")