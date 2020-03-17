from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import os
import pandas as pd
import random

# DOWNLOAD_PATH = "C:\\Users\\kristian.jackson\\Downloads\\Reports"
DOWNLOAD_PATH = os.getcwd() + '\\DOWNLOADS'


def download_wait(path_to_downloads):
    seconds = 0
    dl_wait = True
    while dl_wait and seconds < 20:
        time.sleep(1)
        dl_wait = False
        for fname in os.listdir(path_to_downloads):
            if fname.endswith('.crdownload'):
                dl_wait = True
        seconds += 1


def download_reports(agency, report_names):
    f = open("download_log.csv", "a+")
    report_driver = webdriver.Chrome(options=chrome_options)
    print(str(len(report_names)) + ' results found')
    for report_name in report_names:
        report_driver.get(report_name.get_attribute('href'))
        file_link = report_driver.find_element_by_css_selector('span.file a')
        print('Downloading...' + file_link.get_attribute('href'))
        f.write(str(agency) + ', ' + file_link.get_attribute('href') + '\n')
        time.sleep(random.randint(1, 3))
        report_driver.get(file_link.get_attribute('href'))
    download_wait(DOWNLOAD_PATH)
    f.close()
    report_driver.quit()


print(DOWNLOAD_PATH)

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_experimental_option(
    'prefs', {
        "download.default_directory": DOWNLOAD_PATH,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })

agency_list = pd.read_csv('AgencyListing.csv')

print('Read in list of ' + str(len(agency_list)) + ' agencies')

for agency in agency_list['Agency Number'].tolist():

    print("Scraping agency number " + str(agency))

    URL = 'https://www.oversight.gov/reports?field_address_country=AA&field_type_of_product[0]=9&field_component_agency_[0]=' + str(
        agency) + '&items_per_page=60'

    driver = webdriver.Chrome(options=chrome_options)

    print('Starting Scrape')
    driver.get(URL)
    while True:
        report_names = driver.find_elements_by_css_selector(
            'td.st-val.views-field.views-field-title a')
        download_reports(agency, report_names)
        try:
            next_page = driver.find_element_by_css_selector('li.pager-next a')
            print(next_page)
            driver.get(next_page.get_attribute('href'))
            report_names = driver.find_elements_by_css_selector(
                'td.st-val.views-field.views-field-title a')
            download_reports(agency, report_names)
        except:
            print('Finished downloading reports')
            break

    driver.quit()
