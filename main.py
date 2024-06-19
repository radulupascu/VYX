from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re

def parse_products(text):
    # Regex to match product name followed by price and optional negotiability
    # Adjusted to capture:
    # - Any characters that do not immediately precede the specific pattern of price ending in 'lei'
    # - A more specific check for price followed optionally by 'Prețul e negociabil'
    pattern = r"(.+?)(\d[\d\s]*? lei)(\sPrețul e negociabil)?"

    results = []
    for match in re.finditer(pattern, text, re.DOTALL):
        product_name = match.group(1).strip()
        price = match.group(2).strip()
        negotiable = match.group(3) if match.group(3) is not None else ""  # Ensures a clean format if not present

        # Correct formatting for product names that may end up with trailing characters before price
        product_name = re.sub(r'\s*-\s*$', '', product_name)  # Removes any trailing '-' potentially left before the price

        # Format the result with a space between product name and price
        formatted_result = f"{product_name} {price}{negotiable}"
        results.append(formatted_result)

    return results

def format_product_info(text):
    # Insert a space between the product name and the price
    text = re.sub(r'(\D)(\d+lei)', r'\1 \2', text)

    # Ensure there is a space after 'lei'
    text = re.sub(r'(lei)(?!\s|$)', r'\1 ', text)

    # Add a space after 'Prețul e negociabil' if not followed by a newline or end of string
    text = re.sub(r'(Prețul e negociabil)(?!\s|$)', r'\1 ', text)

    return text


def get_html_with_selenium(url):
    options = Options()
    options.add_argument("--headless")  # Runs Chrome in headless mode.
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')

    # Specify the path to chromedriver using Service
    s = Service('/opt/homebrew/bin/chromedriver')
    driver = webdriver.Chrome(service=s, options=options)
    
    driver.get(url)
    # Wait for the page to load completely
    driver.implicitly_wait(10)  # seconds
    
    # This will get the initial HTML of the page, you can navigate or interact with the page if required
    html_content = driver.page_source
    
    driver.quit()
    return html_content

def correct_year_price(text):
    # Use a regular expression to identify cases where '2024' is followed by another digit and a price
    # This regex will capture '20242 900 lei' as ('2024', '2', '900')
    corrected_text = re.sub(r'(2024)(\d)\s+(\d+)\s+lei', lambda m: f"{m.group(1)} {m.group(2)}{m.group(3)} lei", text)

    return corrected_text

def add_newline_after_date(text):
    # List of Romanian months
    romanian_months = [
        "ianuarie", "februarie", "martie", "aprilie", "mai", "iunie",
        "iulie", "august", "septembrie", "octombrie", "noiembrie", "decembrie"
    ]

    # Regex to match any Romanian month followed by 2024
    pattern = r'(' + '|'.join(romanian_months) + r')\s+2024'

    # Replace matched pattern with itself followed by a newline
    formatted_text = re.sub(pattern, r'\1 2024\n', text)

    return formatted_text

def separate_product_price(text):
    # This regex finds a sequence including letters, punctuation, and parentheses, followed by an optional digit glued to the name, and a price
    formatted_text = re.sub(r'([a-zA-Z\.\,\(\)]+)(\d*)\s*(\d+\s*lei)', r'\1 ~~ \2\3', text)

    # This additional regex ensures that if there is no digit glued to the name, the format is still correct
    formatted_text = re.sub(r'([a-zA-Z\.\,\(\)]+)\s+(\d+\s*lei)', r'\1 ~~ \2', formatted_text)

    return formatted_text

def remove_first_and_last_line(text):
    lines = text.split('\n')  # Split the string by newlines
    if len(lines) > 2:
        lines = lines[2:-1]  # Remove the first and last lines
    return '\n'.join(lines)  # Join the remaining lines back into a single string



def parse_and_replace(text):
    # Replace 'Salvează ca favorit' with a space
    formatted_text = text.replace('Salvează ca favorit', '')
    formatted_text = formatted_text.replace('PROMOVAT', 'PROMOVAT ~~ ')
    formatted_text = formatted_text.lower().replace('placa video', '')
    formatted_text = formatted_text.lower().replace('vand', '')
    formatted_text = formatted_text.lower().replace('negociabil', '')

    # Append a newline character after '2024'
    # formatted_text = formatted_text.replace('2024', '2024\n')
    formatted_text = formatted_text.replace('leiNou', 'lei ~~ NU ~~ NOU ~~ ')
    formatted_text = formatted_text.replace('leiUtilizat', 'lei ~~ NU ~~ UTILIZAT ~~ ')
    formatted_text = formatted_text.replace('leiPrețul e negociabil', 'lei NEGOCIABLIL ')
    formatted_text = formatted_text.replace('lei NEGOCIABLIL Utilizat', 'lei ~~ NEGOCIABLIL ~~ UTILIZAT ~~ ')
    formatted_text = formatted_text.replace('lei NEGOCIABLIL Nou', 'lei ~~ NEGOCIABLIL ~~ NOU ~~ ')
    formatted_text = formatted_text.replace('lei NEGOCIABLIL ', 'lei ~~ NEGOCIABLIL ~~ ')
    

    # Append a newline character after times in the format 'xx:xx'
    formatted_text = re.sub(r'(\d{2}:\d{2})', r'\1\n', formatted_text)

    return formatted_text

def add_newline_after_phrase(text):
    # Append a newline character after 'pentru tine'
    formatted_text = text.replace('pentru tine', 'pentru tine\n')

    return formatted_text

if __name__ == '__main__':
    page_number = 3
    # URL of the category page
    # url = 'https://www.olx.ro/electronice-si-electrocasnice/componente-laptop-pc/placi-video/?currency=RON'
    url = f'https://www.olx.ro/electronice-si-electrocasnice/componente-laptop-pc/placi-video/?currency=RON&page={page_number}'
    html_content = get_html_with_selenium(url)

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')

    # Extracting all text within <div> tags
    div_texts = [div.get_text(strip=True) for div in soup.find_all('div')]

    # Extracting specific elements, e.g., inputs within a specific class
    input_values = [input.get('value', '') for input in soup.select('input[type="text"]')]  # Adjusted to avoid KeyError

    # Call the function to parse and replace
    parsed_text = parse_and_replace(div_texts[1])
    # parsed_text = conditional_newline(parsed_text)
    parsed_text = add_newline_after_phrase(parsed_text)
    parsed_text = separate_product_price(parsed_text)
    parsed_text = add_newline_after_date(parsed_text)
    parsed_text = correct_year_price(parsed_text)
    parsed_text = remove_first_and_last_line(parsed_text)
    # parsed_products = parse_products(parsed_text)


    # # Save the list of div texts to a file
    # div_texts_path = 'div_texts.txt'
    # with open(div_texts_path, 'w', encoding='utf-8') as file:
    #   for product in parsed_products:
    #     file.write(product + '\n')

    # Save the HTML content to a file
    products_path = 'products.txt'
    with open(products_path, 'w', encoding='utf-8') as file:
        file.write(parsed_text)

    print(f"Products have been written to {products_path}")
    # print(f"Div texts have been written to {div_texts_path}")

