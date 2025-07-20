from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time

options = Options()
# comment out for visible browser
options.add_argument("--headless")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver.get("https://www.zeptonow.com/search?query=Lay%27s+chips")

time.sleep(5)
products = driver.find_elements(By.XPATH, "//a[contains(@class, 'group')]")

for product in products:
    try:
        name = product.find_element(By.XPATH, ".//h5").text
        discounted_price = product.find_element(
            By.XPATH,
            ".//p[contains(text(), '₹')]"
        ).text

        # Check if original price exists
        original_price_elements = product.find_elements(
            By.XPATH,
            ".//p[contains(@class, 'line-through') and contains(@class, 'text-[#757C8D]')]"
        )
        original_price = original_price_elements[0].text if original_price_elements else "N/A"

        print(f"{name} | Discounted: {discounted_price} | Original: {original_price}")
    except Exception as e:
        print("Skipping one product due to error:", e)
