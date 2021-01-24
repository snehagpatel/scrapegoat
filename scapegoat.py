import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import os
import csv

seconds = 5
shorter_seconds = 2
longer_seconds = 10


def check_exists_by_xpath(drive, xpath):
    try:
        drive.find_element_by_xpath(xpath)
    except NoSuchElementException:
        return False
    return True

## searches for input elements, fills info, and logs in 
def login(drive, email, psswrd):
    username = drive.find_element_by_name('user[email]')
    password = drive.find_element_by_name('user[password]')
    username.send_keys(email)
    password.send_keys(psswrd)
    drive.find_element_by_id('submit-button').click()


## search for specific ticker once logged in
def tick_search(drive, tck):
    ticker_search = drive.find_element_by_xpath("//input[@data-test='ticker-search']")
    ticker_search.send_keys(tck)
    ticker_search.send_keys(Keys.ENTER)
    print('Looking up: ' + tck)


## start at splash page
## takes list of ticker names, searches them, and outputs a list of their links
def article_links(drive, ticker_list):
    links = []
    for ticker in ticker_list:
        # given_ticker_hrefs = []
        tick_search(drive, ticker)
        time.sleep(seconds)
        ## checks if company hits exists
        search_results = drive.find_element_by_xpath('//div[@data-test="transcript-search-results"]')
        label_left = search_results.find_element_by_xpath('.//span').text
        if 'Company' in label_left:
            company = driver.find_elements_by_tag_name("div")[72]
            files = company.find_elements_by_xpath('.//a[starts-with(@id,"transcript-item")]')
            given_ticks_hrefs = [f.get_attribute('href') for f in files]
            links = links + given_ticks_hrefs
            print('Saving links for ' + ticker + '...')
        else:
            print('No links found for ' + ticker)
        drive.get('*INSERT SPLASH PAGE URL HERE*')
        time.sleep(shorter_seconds)
    return links


        

### Main
 
## open and read tickers.csv to make python list
df = open('/Users/**UserAcctName**/Desktop/scapegoat/tickers.csv', 'r')
reader = csv.reader(df)
tickers = []
for row in reader:
    if row not in tickers:
        tickers = tickers + row
del tickers[0]
print('Ticker list created')

## Logging in
driver = webdriver.Chrome()
driver.get('*INSERT SPLASH PAGE URL HERE*')
time.sleep(seconds)
login(driver, 'insertemail@email.com', '*******')
print('Logging In')

time.sleep(seconds)


# Retrieve articles for desired tickers
link_lst = article_links(driver, tickers)

# Use for first time running to resume later:
'''
with open('links.txt', 'w') as f:
    for l in link_lst:
        f.write('%s\n' % l)
'''

### Resume code using this:
'''
driver = webdriver.Chrome()
driver.get('*INSERT SPLASH PAGE URL HERE*')
time.sleep(seconds)
login(driver, 'insertemail@email.com', '*******')
print('Logging In')

time.sleep(seconds)

with open('/Users/**UserAcctName**/Desktop/links.txt', 'r') as f:
	links = f.read()
link_lst = links.split('\n')
del link_lst[:1869]
'''

for lnk in link_lst:


    driver.get(lnk)
    time.sleep(longer_seconds)
    t = lnk.split('-')[-1]
    path = "/Users/**UserAcctName**/Desktop/scapegoat/"
    ticker_folder = path + t
    if not os.path.exists(ticker_folder):
        os.makedirs(ticker_folder)

    file_name = t + str(link_lst.index(lnk) + 1870)
    print(file_name + ' loaded')
    html_name = path + t + '/' + file_name + ".html"
    
    with open(html_name, "w") as f:
        f.write(driver.page_source)


driver.quit()
