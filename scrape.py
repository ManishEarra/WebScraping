import pandas as pd
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
import time
import json
from selenium.webdriver.support.wait import WebDriverWait

def download_data():

    """ Assumed the CSV file is in my current working directory. Read CSV file to get Country Code and Asin parameters for URL."""

    path = os.path.join(os.getcwd(), "Amazon Scraping - Sheet1.csv")

    data_frame = pd.read_csv(path)

    print(data_frame.head())


    def create_driver():
        """
        Creates a Chrome Driver.

        Returns
        --------
        driver : driver
            chrome web driver.
        """
        chrome_options = Options()
        chrome_options.add_argument("start-maximized")
        # chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(
            executable_path=r'./chromedriver.exe', options=chrome_options)
        return driver

    # send a get request to the page, and if the status code is 404
    # returns False.

    def valid_url(url):
        req = requests.head(url)
        print(req.status_code)
        if req.status_code != 404:
              return True
        return False



    country = "" # base country code.
    asin = "" # default Asin parameter.

    count = 100 # To check the count of Url's.
    result = [] # To store data of all the products.
    start = time.time()
    """Accessing each row in the data frame using index to get Country code and Asin parameters"""
    for ind in data_frame.index:
        count -= 1 # Reducing the count value for each row in the data frame.
        if count > 0:
            # print((data_frame['Asin'][ind]), (data_frame['country'][ind]))
            country = data_frame['country'][ind]
            asin = data_frame['Asin'][ind]
            """ Base url to scrape data."""
            base_url = f"https://www.amazon.{country}/dp/{asin}"
            bool = valid_url(base_url)
            # If the URL is not valid i,.e if the status code is 404. Prints that url along with 404 error found text.
            # Else will try to get data if possible.
            if not bool:
                print("404 Error found : ", base_url)
                continue
            else:
                print(base_url)
                driver = create_driver()
                driver.get(base_url)
                try:
                    product = {} # dictionary to store required data of a product
                    wait = WebDriverWait(driver, timeout=5)
                    title = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="productTitle"]')))
                    # Waiting for 5 sec to see whether the required element is loaded or not.
                    # print("Title : ",title.text)
                    product["Product Title"] = title.text
                    image_block = driver.find_element(By.ID, "imageBlock")
                    image_url = image_block.find_element(By.TAG_NAME,'img').get_attribute("src")
                    # print("Image_url : ", image_url)
                    product["Product Image URL"] = image_url
                    price = driver.find_element(By.XPATH,'//*[@id="corePriceDisplay_desktop_feature_div"]/div[1]')
                    # print("Price : ",price.text)
                    product["Price of the Product"] = price.text
                    details = driver.find_element(By.XPATH,'//*[@id="prodDetails"]/div/div[1]/div[1]/div/div[2]/div/div').text
                    # print("Details : ", details)
                    product["Product Details"] = details
                    result.append(product) # Appending(adding) data of a Product in a dictionary to the list.
                    # print(ind," : ",product)
                    # driver.close()
                except:
                    pass # Skipping URLS(not working)
                try:
                    product = {}
                    wait = WebDriverWait(driver, timeout=5)
                    title = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="productTitle"]')))
                    # Waiting for 5 sec to see whether the required element is loaded or not.
                    # print("Title : ",title.text)
                    product["Product Title"] = title.text
                    image_block = driver.find_element(By.ID, "imageBlock")
                    image_url = image_block.find_element(By.TAG_NAME,'img').get_attribute("src")
                    # print("Image_url : ", image_url)
                    product["Product Image URL"] = image_url
                    price_element = driver.find_element(By.CLASS_NAME,'swatchElement.selected.resizedSwatchElement')
                    price = price_element.find_element(By.CLASS_NAME,'a-color-base')
                    # print("Price : ",price.text)
                    product["Price of the Product"] = price.text
                    details = driver.find_element(By.ID,'detailBullets_feature_div').text
                    # print("Details : ", details)
                    product["Product Details"] = details
                    result.append(product) # Appending(adding) data of a Product in a dictionary to the list.
                    # print(ind," : ",product)
                except:
                    pass # Skipping URLS(not working)

                driver.close()
                # Closing driver after each iteration.

    end = time.time()
    print("Time taken for 100 URLS : ", (end-start))
    print("Total number of products scraped : ",len(result))
    json_object = json.dumps(result) # Converts resultant dictionary to Json Object.
    return json_object

if __name__ == "__main__":
    Json_object = download_data()