from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time
import os

URL = 'https://www.oversight.gov/reports?field_address_country=AA&field_type_of_product[0]=9&field_component_agency_[0]=395&items_per_page=60'
DOWNLOAD_PATH = "C:\\Users\\kristian.jackson\\Downloads\\Reports"


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


def download_reports(report_names):
    report_driver = webdriver.Chrome(options=chrome_options)
    print(str(len(report_names)) + ' results found')
    for report_name in report_names:
        report_driver.get(report_name.get_attribute('href'))
        file_link = report_driver.find_element_by_css_selector('span.file a')
        print('Downloading...' + file_link.get_attribute('href'))
        report_driver.get(file_link.get_attribute('href'))
    download_wait(DOWNLOAD_PATH)
    report_driver.quit()


chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_experimental_option(
    'prefs', {
        "download.default_directory": DOWNLOAD_PATH,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "plugins.always_open_pdf_externally": True
    })

driver = webdriver.Chrome(options=chrome_options)

print('Starting Scrape')
driver.get(URL)
while True:
    report_names = driver.find_elements_by_css_selector(
        'td.st-val.views-field.views-field-title a')
    download_reports(report_names)
    try:
        next_page = driver.find_element_by_css_selector('li.pager-next a')
        print(next_page)
        driver.get(next_page.get_attribute('href'))
        report_names = driver.find_elements_by_css_selector(
            'td.st-val.views-field.views-field-title a')
        download_reports(report_names)
    except:
        print('Finished downloading reports')
        break

driver.quit()
