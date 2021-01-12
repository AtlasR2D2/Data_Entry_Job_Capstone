import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import os

chrome_driver_path = r'chromedriver.exe'

driver = webdriver.Chrome(executable_path=chrome_driver_path)

GOOGLE_FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfddvsTEvDuS0spM_5wha5ixOnsDiMRFcv4dvAhCRQ-gWuX8Q/viewform?usp=sf_link"

GOOGLE_FORM_VIEW_URL = "https://docs.google.com/spreadsheets/d/1HM2-N1E54S_NbTGKmdFUrG8ZQLPTHUe1BQtZIck9y9k/edit?usp=sharing"

ZILLOW_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"

address_q_text = "What's the address of the property?"

price_q_text = "What's the price per month?"

link_q_text = "What's the link to the property?"

q_text_dict = {
    "address": address_q_text,
    "price": price_q_text,
    "link": link_q_text
}

# -----------------------------------------------------------------------------------------------------
# Get Property Details from Zillow
driver.get(ZILLOW_URL)

html = driver.page_source

soup = BeautifulSoup(html, "html.parser")
property_list = soup.find_all(name="article", class_="list-card")
property_details = []
for article in property_list:
    article_link = article.find(name="a")["href"]
    article_price = article.find(name="div", class_="list-card-price").getText()
    article_address = article.find(name="address", class_="list-card-addr").getText()
    property_details.append(
        {
            "address": article_address,
            "price": article_price,
            "link": article_link
        }
    )

# -----------------------------------------------------------------------------------------------------
# Upload property_details to Google Form

driver.get(GOOGLE_FORM_URL)

time.sleep(2)


def initialise_form_elements_dict():
    """returns a dictionary containing the form elements"""
    return {

        "inputs": {
            "address": driver.find_element_by_xpath("//*[@id=\"mG61Hd\"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input"),
            "price": driver.find_element_by_xpath("//*[@id=\"mG61Hd\"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input"),
            "link": driver.find_element_by_xpath("//*[@id=\"mG61Hd\"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input")
        },
        "buttons": {
            "submit": driver.find_element_by_xpath("//*[@id=\"mG61Hd\"]/div[2]/div/div[3]/div[1]/div/div")
        }

    }


property_count = 0
for property_x in property_details:
    if property_count > 0:
        # Submit another response
        driver.find_element_by_link_text("Submit another response").click()
        time.sleep(2)
    # Re-initialise elements dictionary
    g_form_elements_dict = initialise_form_elements_dict()
    # Load Property Details to inputs dictionary
    property_inputs = {
        "address": property_x["address"],
        "price": property_x["price"],
        "link": property_x["link"]
    }
    # Add Answers for property_x to Google Form
    for input_type in g_form_elements_dict["inputs"].keys():
        g_form_elements_dict["inputs"][input_type].send_keys(property_inputs[input_type])
    # Submit Answer
    g_form_elements_dict["buttons"]["submit"].click()
    time.sleep(2)
    # Increment Property Counter
    property_count += 1

# Show Spreadsheet Results
driver.get(url=GOOGLE_FORM_VIEW_URL)