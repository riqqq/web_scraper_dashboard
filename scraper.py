from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time

# Configure Chrome options
chrome_options = Options()
chrome_options.add_argument("--headless")  # Optional: run in headless mode
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")

# Configure the webdriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)

def scrape_data():
    driver.get('https://www.bbc.com/news')  # Target website

    # Scraping headlines
    data = []

    # Selector for headlines
    elements = driver.find_elements(By.CSS_SELECTOR, 'h2.sc-4fedabc7-3.zTZri')
    for element in elements:
        print("Found some element")
        if element.text:  # Ensure the text is not empty
            data.append(element.text)

    # Remove duplicates
    data = list(set(data))

    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['Headline'])
    df.to_csv('headlines.csv', index=False)

    driver.quit()

if __name__ == "__main__":
    scrape_data()
