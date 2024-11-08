from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Initialize the Edge WebDriver
driver = webdriver.Edge()
driver.get("https://www.amazon.in/s?rh=n%3A6612025031&fs=true&ref=lp_6612025031_sar")

# Check if the page shows a "busy" message
time.sleep(2)  # Allow time for the page to load
try:
    busy_message = driver.find_element(By.XPATH, "//h4[contains(text(), 'Oops!')]").text
    if "Oops!" in busy_message:
        print("Amazon.in is currently experiencing high traffic. Please try again later.")
        driver.quit()
        exit()
except Exception as e:
    pass  # If no "busy" message is found, continue with scraping

# Lists to store product details
product_names = []
prices = []
ratings = []
sellers = []

# Locate product items on the page
product_elements = driver.find_elements(By.CSS_SELECTOR, "div.s-main-slot div.s-result-item")

# Extract details from each product
for product in product_elements:
    # Extract product name
    try:
        product_name = product.find_element(By.CSS_SELECTOR, "h2 a span").text
    except:
        product_name = "N/A"
    product_names.append(product_name)

    # Extract price
    try:
        price = product.find_element(By.CSS_SELECTOR, "span.a-price-whole").text
    except:
        price = "N/A"
    prices.append(price)

    # Extract rating
    try:
        rating_text = product.find_element(By.CSS_SELECTOR, "i.a-icon.a-icon-star-small").get_attribute("class")
        rating = int(rating_text.split('-')[-1])  # Extract the rating from the class name
    except:
        rating = "N/A"
    ratings.append(rating)

    # Wait for the seller name element to be present
    try:
    # Locate the seller name using the span directly
        seller_name = WebDriverWait(product, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "span.a-size-base.a-color-base"))
    ).text.strip()  # Use .strip() to remove any leading/trailing whitespace
    except Exception as e:
        print("Error:", e)
        seller_name = "N/A"
    # Append the seller name to the sellers list
    sellers.append(seller_name)

# Close the driver after scraping is complete
driver.quit()

# Create a DataFrame with specified column headers
data = pd.DataFrame({
    "Product Name": product_names,
    "Price": prices,
    "Rating": ratings,
    "Seller Name (If not out of stock)": sellers
})

# Save the DataFrame to a CSV file in tabular format
data.to_csv("amazon_products.csv", index=False, sep=',', encoding='utf-8')
print("Data successfully saved to amazon_products.csv")

# Print a sample of the data in tabular format for confirmation
print("\nSample data preview:")
print(data.head(10).to_string(index=False))