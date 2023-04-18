'''
This code is used to web-scrape the ESG reports in HKEX

'''

from selenium import webdriver
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from lxml import etree
import os, re, glob, csv

input_time=["2021-07-05 to 2022-07-05", "2020-07-06 to 2021-07-06","2019-07-05 to 2020-07-05", "2018-07-08 to 2019-07-08",
            "2017-07-08 to 2018-07-08","2016-07-10 to 2017-07-10","2015-07-10 to 2016-07-10", "2014-07-10 to 2015-07-10",
            "2013-07-10 to 2014-07-10", "2012-07-10 to 2013-07-10"]

def clean(str):
    '''
    function used to clean and formate a string
    :param string: str, input string
    :return: str, cleaned string
    '''
    str = str.replace("\xa0", " ")
    str = ''.join(str).strip()
    str = str.replace("\n", "/")
    str = re.sub(' +', ' ', str)
    return str

def open_browser(url):
    '''
    function used to call the selelium webdriver and open the given url
    :param url: str, a weblink
    :return: open the chrome and load the webpage
    '''
    driver.get(url)
    time.sleep(2)
    driver.maximize_window()


def get_item():
    '''
    function used to check how many time should the webpage load to present a comprehensive list
    :return: int, the total times the page should load
    '''
    number = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                        "#recordCountPanel2 > div.search-results__content-loadmore.component-loadmore.component-loadmore-no-options > div > div.component-loadmore-leftPart__container")))
    i = re.findall(r"\d{3,}", number.text)
    total_load_time=int(int(i[1])/100)+1
    return total_load_time

def load_more(n):
    '''
    function used to execute the 'load more'
    :param n: int, times the page should load 
    :return: the page will load for n times
    '''
    for i in range(n-1):
        time.sleep(3)
        number = WebDriverWait(driver, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#recordCountPanel2 > div.search-results__content-loadmore.component-loadmore.component-loadmore-no-options > div > div.component-loadmore-leftPart__container")))

        print(number.text)

        time.sleep(2)
        load = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,
                                            "#recordCountPanel2 > div.search-results__content-loadmore.component-loadmore.component-loadmore-no-options > div > div.component-loadmore__dropdown-container > ul > li > a")))
        load.click()


def get_specific_info():
    table = WebDriverWait(driver, 100).until(
        EC.presence_of_element_located((By.CSS_SELECTOR,
                                            "#titleSearchResultPanel > div > div.title-search-result.search-page-container > div.table-scroller-container > div.table-scroller > table > tbody")))

    rows = WebDriverWait(table, 100).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR,
                                             "tr")))

    print("There are totally " + str(len(rows)) + " rows")

    info_dict = {}
    counter=1
    for row in rows:
        time.sleep(0.5)
        release_time = WebDriverWait(row, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            "td.text-right.release-time"))).text

        stock_code = WebDriverWait(row, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            "td.text-right.stock-short-code"))).text
        stock_code=clean(stock_code)

        stock_short_name = WebDriverWait(row, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR,
                                            "td.stock-short-name"))).text
        stock_short_name=clean(stock_short_name)

        report_type=WebDriverWait(row, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.doc-link"))).text

        report_url = WebDriverWait(row, 100).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.doc-link [href]"))).get_attribute("href")

        # to exclude reports that's not ESG report
        if "environment" not in report_type.lower():
            print("This is not wanted obs")
        elif "social" not in report_type.lower():
            print("This is not wanted obs")
        elif "sustainability" not in report_type.lower():
            print("This is not wanted obs")
        elif "csr" not in report_type.lower():
            print("This is not wanted obs")
        if "annual report" in report_type.lower():
            print("This is not wanted obs")
        else:
            info_dict["release_time"] = release_time
            info_dict["stock_code"] = stock_code
            info_dict["stock_short_name"] = stock_short_name
            info_dict["report_url"] = report_url
            info_dict["report_type"]=report_type

            save_info(info_dict)

        print('Progress：', f'{counter}/{len(rows)}')
        counter += 1


def save_info(info_dct):
    '''
    function used to write the obs in a csv file
    :param info_dct: dict, a dictionary contain the scraped information
    :return: saved csv file
    '''
    with open('.\hkexesg_2023.csv', 'a+', newline='', encoding='utf-8') as f:
        header = ['release_time', 'stock_code', 'stock_short_name', 'report_url', "report_type"]
        f_csv = csv.DictWriter(f, fieldnames=header)

        f_csv.writerow(info_dct)
    print('this obs is written in the csv file')


if __name__ == "__main__":
    options = webdriver.ChromeOptions()
    options.add_experimental_option('prefs', {
        "download.default_directory": r".\download",  # Change default directory for downloads
        "download.prompt_for_download": True,  # To auto download the file
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True  # It will not open PDF directly in chrome
    })
    chromedriver = "/Users/irene/Desktop/Coding/Webdriver/chromedriver_mac/chromedriver" 
    driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)

    basic_url = "https://www1.hkexnews.hk/search/titlesearch.xhtml?lang=en"

    open_browser(basic_url)

    total_load_time=get_item()
    
    print("loading for "+str(total_load_time-1)+" times ...")
    
    load_more(total_load_time)
    time.sleep(5)

    #scroll down the page
    driver.execute_script("window.scrollTo(0, 2000)")
    driver.execute_script("window.scrollTo(0, 500)")
    driver.execute_script("window.scrollTo(0, 0)")
    time.sleep(10)

    get_specific_info()






