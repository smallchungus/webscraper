from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup as bs
import re
import time
import pandas as pd

PATH = input("Enter the Webdriver path: " )
USERNAME = input("Enter the username: ")
PASSWORD = input("Enter the password: ")
print(PATH)
print(USERNAME)
print(PASSWORD)

driver = webdriver.Chrome(PATH)

driver.get("https://www.linkedin.com/uas/login")
time.sleep(3)

email=driver.find_element_by_id("username")
email.send_keys(USERNAME)
password=driver.find_element_by_id("password")
password.send_keys(PASSWORD)
time.sleep(3)
password.send_keys(Keys.RETURN)

# Create a wait object with a timeout (in seconds)
wait = WebDriverWait(driver, 10)

# Use the wait object to wait until the search input box is clickable
search_input = wait.until(
    EC.element_to_be_clickable((By.CLASS_NAME, "search-global-typeahead__input"))
)
# Locate the search input box using its class name
search_input = driver.find_element_by_class_name("search-global-typeahead__input")

# Read the CSV
df = pd.read_csv("C:\Users\wchen\OneDrive\Documents\GitHub\webscraper\combined.csv")

# List of roles you want to combine with the organization names
roles = ["director", "associate director", "CEO", "board of directors"]

# Loop through each organization name
for org_name in df["Name of Organization"]:
    for role in roles:
        # Combine the organization name with the role for the search query
        search_query = f"{org_name} {role}"

        # Wait for the search input to be clickable
        search_input = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "search-global-typeahead__input"))
        )

        # Clear any previous text and input the search query
        search_input.clear()
        search_input.send_keys(search_query)

        # Submit the search
        search_input.send_keys(Keys.RETURN)

        # Wait for search results to load (you can adjust the wait time as needed)
        time.sleep(5)
