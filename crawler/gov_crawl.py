from selenium import webdriver
import time
import random
import sys
import os
from pyvirtualdisplay import Display

try:
    target_folder_name = sys.argv[1]
except IndentationError as e:
    print('NEED FOLDER NAME')
    sys.exit(1)

display = Display(visible=0, size=(800, 600))
display.start()

driver_path = './chromedriver'
driver = webdriver.Chrome(driver_path)


max_page_number = 2386
base_url = 'http://www.gov.kr/portal/orgSite?pageIndex='

file_path = os.path.expanduser('~') + '/Documents/keyword/' + target_folder_name + '/'

if not os.path.exists(file_path):
    os.makedirs(file_path)

for index in range(1, max_page_number + 1):

    try:
        page_url = base_url + str(index)
        driver.get(page_url)
        driver.implicitly_wait(10)

        #print(soup.prettify())
        file_name = str(index)+'.html'
        f=open(file_path+file_name, 'w')
        f.write(str(driver.page_source))
        f.close()
        print(driver.title)
        time.sleep(random.randrange(3,7))

    except Exception as e:
        print(e)
        continue

driver.quit()
