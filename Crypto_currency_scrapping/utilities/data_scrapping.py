import time

import pyperclip
from selenium.webdriver.support import expected_conditions as ec

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def scrape_data(name):
    # try:
    options = Options()
    options.add_experimental_option("detach", True)

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    driver.get("https://coinmarketcap.com")
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)  # You can adjust the timeout as needed

    # Click on dummy search
    dummy_search_element = wait.until(
        ec.presence_of_element_located((By.XPATH, '//div[contains(@class, "search-input-static")]')))
    dummy_search_element.click()

    # Search Element
    # click on search element
    search_element = wait.until(ec.presence_of_element_located(
        (By.XPATH,
         '//input[contains(@placeholder, "Search coin, pair, NFT, contract address, exchange, or post")]')))
    # type text
    search_element.send_keys(name)

    time.sleep(5)

    # wait until dropdown is loaded
    wait.until(
        ec.presence_of_element_located((By.XPATH, "//div[@class='tippy-content']")))
    # Press enter
    search_element.send_keys(Keys.ENTER)

    wait.until(ec.presence_of_element_located(
        (By.XPATH, "//div[contains(@class, 'sc-d1ede7e3-0 gNSoet flexStart alignBaseline')]")))

    wait.until(ec.presence_of_element_located((By.XPATH, "//body")))

    # Price
    price_main_element = wait.until(
        ec.presence_of_element_located((By.XPATH, "//div[contains(@class, 'sc-d1ede7e3-0 eaAjIS coin-stats-header')]")))

    price = "&00"
    try:
        price = price_main_element.find_element(By.XPATH, '//div[contains(text(), "$")]').text

    except:
        price = price_main_element.find_element(By.XPATH, '//span[contains(text(), "$")]').text

    # Price change
    price_change_element = \
        wait.until(
            ec.presence_of_element_located((By.XPATH, "//p[contains(@class, 'sc-71024e3e-0')]")))

    price_change = price_change_element.text.split()[0]

    if price_change_element.get_attribute("color") == "red":
        price_change = "-" + price_change

    # Coin Matrix table element

    matrix_table_element = wait.until(ec.presence_of_element_located(
        (
            By.XPATH,
            "//dl[@class='sc-d1ede7e3-0 bwRagp coin-metrics-table'][//div[@class= 'sc-d1ede7e3-0 bwRagp']]")))

    # Coin Matrix table list of elements
    list_matrix_element = matrix_table_element.find_elements("xpath",
                                                             "//div[@class= 'sc-d1ede7e3-0 bwRagp']//div[@class= 'sc-d1ede7e3-0 sc-cd4f73ae-0 bwRagp iWXelA flexBetween']")
    # Market cap
    market = list_matrix_element[0]
    market_cap_array = market.find_element("xpath", "//dd[contains(text(),'$')]").text.split('\n')
    market_cap = market_cap_array[1].replace("$", "")

    # Market cap rank
    market_cap_rank = market.find_element("xpath", "//span[@class= 'text slider-value rank-value']").text.replace(
        "#",
        "")

    volume_element = list_matrix_element[1]

    volume = volume_element.find_element(By.XPATH, ".//dd[contains(text(),'$')]").text.split('\n')
    volume_info = volume[0].replace("$", "")

    # Volume_rank
    volume_rank = wait.until(
        ec.presence_of_element_located((By.XPATH, ".//span[@class='text slider-value rank-value']"))
    ).text.replace("#", "")

    # Volume change
    volume_change = list_matrix_element[2].find_element(By.XPATH, ".//dd[contains(text(),'%')]").text

    circulating_supply = \
        list_matrix_element[3].find_element(By.XPATH, ".//dd[@class='sc-d1ede7e3-0 hPHvUM base-text']").text.split(
            ' ')[0]

    total_supply = \
        list_matrix_element[4].find_element(By.XPATH, ".//dd[@class='sc-d1ede7e3-0 hPHvUM base-text']").text.split(
            ' ')[0]

    diluted_market_cap = \
        list_matrix_element[5].find_element(By.XPATH, ".//dd[@class='sc-d1ede7e3-0 hPHvUM base-text']").text.split(
            ' ')[0]

    parent_element = wait.until(
        ec.presence_of_element_located((By.XPATH, "//div[@class= 'sc-d1ede7e3-0 cvkYMS coin-info-links']")))
    child_elements = parent_element.find_elements("xpath", "//div[@class= 'sc-d1ede7e3-0 jTYLCR']")
    counter = 0

    # Contacts
    contacts = []

    elements_with_text = child_elements[counter].find_elements(By.XPATH, "//span[contains(text(), 'Contracts')]")

    if elements_with_text:
        list_contact_element = child_elements[counter].find_elements("xpath",
                                                                     "//div[@class= 'sc-d1ede7e3-0 sc-7f0f401-0 sc-96368265-0 bwRagp gQoblf eBvtSa flexStart']")
        for contact_element in list_contact_element:
            contact_name = contact_element.find_element("xpath", ".//span[@class= 'sc-71024e3e-0 dEZnuB']")
            contact_name = contact_name.text.replace("&nbsp;", "").replace(":", "")

            # Copy address from clipboard
            copy_element = contact_element.find_element("xpath", ".//div[@class= 'BasePopover_base__tgkdS']")
            copy_element.click()
            contact_address = pyperclip.paste()

            contacts.append({
                "name": contact_name,
                "address": contact_address
            })
        counter += 1

    # official elements
    elements_with_text = child_elements[counter].find_elements(By.XPATH, "//span[contains(text(), 'Official links')]")
    official = []
    if elements_with_text:
        official_elements = child_elements[counter].find_elements("xpath",
                                                                  ".//div[@class= 'sc-d1ede7e3-0 sc-7f0f401-0 gRSwoF gQoblf']")

        for official_link in official_elements:
            url = official_link.find_element("xpath", ".//a[@rel='nofollow noopener']").get_attribute("href")

            name = official_link.find_element("xpath", ".//a[@rel='nofollow noopener']")
            name = driver.execute_script("return arguments[0].textContent;", name)

            official.append({
                "name": name,
                "url": url

            })
        counter += 1

    # Social elements
    elements_with_text = child_elements[counter].find_elements(By.XPATH, "//span[contains(text(), 'Socials')]")

    social = []
    if elements_with_text:
        social_elements = child_elements[counter].find_elements("xpath",
                                                                ".//div[@class= 'sc-d1ede7e3-0 sc-7f0f401-0 gRSwoF gQoblf']")

        social = []
        for social_link in social_elements:
            url = social_link.find_element("xpath", ".//a[@rel='nofollow noopener']").get_attribute("href")

            name = social_link.find_element("xpath", ".//a[@rel='nofollow noopener']")
            name = driver.execute_script("return arguments[0].textContent;", name)

            social.append({
                "name": name,
                "url": url

            })

    output = {
        "price": price,
        "price_change": price_change,
        "market_cap": market_cap,
        "market_cap_rank": market_cap_rank,
        "volume": volume_info,
        "volume_rank": volume_rank,
        "volume_change": volume_change,
        "circulating_supply": "" if circulating_supply == "--" else circulating_supply,
        "total_supply": "" if total_supply == "--" else total_supply,
        "diluted_market_cap": "" if diluted_market_cap == "--" else diluted_market_cap,
        "contracts": contacts,
        "official_links": official,
        "socials": social
    }

    print(output)
    return output

    # except Exception as e:
    #     print()
    #     return "Error Occur Retry", str(e)


# scrape_data("DUKo")
