from selenium.webdriver import *
import time
import sys
import os
from os import listdir
from os.path import isfile, join
import csv
from settings import *
BASE_PATH = os.path.dirname(os.path.abspath(__file__))


def getWebdriver():
    ##when becomes executable##
    # absolute_path = sys.executable
    # BASE_PATH = os.path.dirname(absolute_path)
    CHROMEDRIVER_PATH = os.path.join(BASE_PATH, 'chromedriver')

    chrome_options = ChromeOptions()
    arguements = [
                '--disable-extensions', '--disable-gpu', '--disable-logging', '--silent',
                  '--log-level=3'
                   # '--headless'
                  ,'--user-data-dir=./User_Data'
                  ]
    for arg in arguements:
        chrome_options.add_argument(arg)
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    dc = DesiredCapabilities.CHROME
    dc['loggingPrefs'] = {'driver': 'OFF', 'server': 'OFF', 'browser': 'OFF'}
    print(CHROMEDRIVER_PATH)
    return Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options, desired_capabilities=dc)



def filter_new_images(path):
    onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
    csv_files = csv.reader(open('data.csv', 'r'))
    d = [row[0] for row in csv_files if row]
    new_files = [val for val in onlyfiles if val not in d]
    return new_files



# Exception handling block
try:
    print('Establishing connection')
    driver = getWebdriver()
    driver.get("https://web.whatsapp.com/")
    driver.maximize_window()
    print('Please scan the Whatsapp QR Code')
    time.sleep(20)


except Exception as ex:
    print('Error in establishing driver connection')
    # driver.quit()
    print('Connection was closed' + str(ex))
    sys.exit()

# Find the conversation of the required contact
user = driver.find_element_by_xpath('//span[@title = "{}"]'.format("JT"))  # Replace user name in the [@title=""]
if user is None:
    print('User not found. Exiting program')
    driver.quit()
    sys.exit()
else:
    user.click()

attachment_box = driver.find_element_by_xpath('//div[@title = "Attach"]')
attachment_box.click()

image_box = driver.find_element_by_xpath(
    '//input[@accept="image/*,video/mp4,video/3gpp,video/quicktime"]')

if not os.path.isabs(image_folder):
    image_folder = os.path.join(BASE_PATH, image_folder)
new_files = filter_new_images(image_folder)
print(str(image_folder))
if new_files:
    for file in new_files:
        print(str(file))
        image_box.send_keys(os.path.join(image_folder, file))
        with open('data.csv', 'a') as fd:
            fd.write('%s\n' % file)

    time.sleep(3)
    send_button = driver.find_element_by_xpath('//span[@data-icon="send-light"]')
    send_button.click()

    time.sleep(10)

# Close the webdriver session
driver.quit()
print('Connection was closed')

