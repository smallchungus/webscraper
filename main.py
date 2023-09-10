from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import logging
from bs4 import BeautifulSoup as bs
import re
import time
import pandas as pd

logging.basicConfig(filename='scraper.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def setup_driver():
    PATH = input("Enter the Webdriver path: ")
    USERNAME = input("Enter the username: ")
    PASSWORD = input("Enter the password: ")
    print(PATH)
    print(USERNAME)
    print(PASSWORD)

    driver = webdriver.Chrome(PATH)
    driver.maximize_window()
    driver.get("https://www.linkedin.com/uas/login")
    time.sleep(3)

    email = driver.find_element_by_id("username")
    email.send_keys(USERNAME)
    password = driver.find_element_by_id("password")
    password.send_keys(PASSWORD)
    time.sleep(3)
    password.send_keys(Keys.RETURN)

    wait = WebDriverWait(driver, 10)
    search_input = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "search-global-typeahead__input")))
    return driver, wait
def search_and_gather_results(org_name, role, driver, wait):
    """Searches for the given role within the organization and gathers the results."""

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

    # Wait for search results to load
    time.sleep(5)

    # Extract the top three results
    results_selector = 'li.reusable-search__result-container'
    results = driver.find_elements_by_css_selector(results_selector)
    top_three_results = results[:3]

    # Define the selectors for the needed data
    name_selector = 'span.entity-result__title-text span span.app-aware-link'
    link_selector = 'span.entity-result__title-text span a.app-aware-link'
    job_title_selector = 'div.entity-result__primary-subtitle.t-14.t-black'

    data = []
    for result in top_three_results:
        try:
            name = result.find_element_by_css_selector(name_selector).text
            link = result.find_element_by_css_selector(link_selector).get_attribute('href')
            job_title = result.find_element_by_css_selector(job_title_selector).text
            data.append({'Name': name, 'Profile_Link': link, 'Job_Title': job_title})
            print(name)
            print(link)
            print(job_title)
        except NoSuchElementException as e:
           logging.error("Exception occurred", exc_info=True)

    return data


def main_process(driver, wait):
    # Read the CSV
    df = pd.read_csv("C:\\Users\\wchen\\OneDrive\\Documents\\GitHub\\webscraper\\combined.csv")
    roles = ["director", "associate director", "CEO", "board of directors"]

    # Initialize results dataframe
    df_results = pd.DataFrame(columns=['Name', 'Profile_Link', 'Job_Title'])

    for org_name in df["Name of Organization"]:
        for role in roles:
            gathered_data = search_and_gather_results(org_name, role, driver, wait)
            df_results = df_results.append(gathered_data, ignore_index=True)

    # Save the results DataFrame to the Downloads folder
    df_results.to_csv('C:\\Users\\wchen\\Downloads\\linkedin_results.csv', index=False)


if __name__ == "__main__":
    driver, wait = setup_driver()
    main_process(driver, wait)
    driver.close()



