from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import pandas as pd
import time
import argparse
import bs4
import numpy as np
import pickle
import urllib3
import warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

if __name__ ==  '__main__':
    ########################################## Get user input ##########################################
    with open('india_cities.pkl', 'rb') as f:
        cities = pickle.load(f)

    parser = argparse.ArgumentParser(description='Scrape info of all restaurants present in a city')
    parser.add_argument('-c', '--city', type=int, default=57, help=f'{cities}')
    args = parser.parse_args()
    input_city = cities[args.city]

    ########################################## Open web browser ##########################################
    ua = UserAgent()
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--incognito')
    chrome_options.add_argument(f"user-agent={ua['google chrome']}")
    driver = uc.Chrome(executable_path=ChromeDriverManager().install(), 
                       options=chrome_options)

    ########################################## Open the main page ##########################################
    driver.get(f'https://www.zomato.com/{input_city}')
    time.sleep(10)

    ########################################## Scrolling the page ##########################################
    scroll_pause_time = 3
    screen_height = driver.execute_script("return window.screen.height;")
    i = 1

    while True:
        driver.execute_script("window.scrollTo(0, {screen_height}*{i});".format(screen_height=screen_height, i=i))
        i += 1
        time.sleep(scroll_pause_time)
        scroll_height = driver.execute_script("return document.body.scrollHeight;")
        if (screen_height) * i > scroll_height:
            break
            
    time.sleep(10)

    ########################################## Scrape restaurant links ##########################################
    source = driver.page_source
    soup = bs4.BeautifulSoup(source, 'html.parser')

    links = []
    for i in soup.find_all('div',{'class':'jumbo-tracker'}):
        try:
            link = i.find('a')['href']
            if('/order' in link):
                links.append(f'https://www.zomato.com{link}')
        except:
            pass
        
    links = [i.split('/order')[0] for i in links]

    print(f'Got {len(links)} restaurants from main page')


    ########################################## Scrape restaurant info ##########################################
    df = []

    for i,link in enumerate(links):
        print(f'Processing {i+1}/{len(links)}')
        driver.get(link)
        time.sleep(10)
        
        try:
            name = str(driver.find_element_by_css_selector('h1').text)
        except:
            name = np.nan
        
        try:
            address = str(driver.find_element_by_xpath('//*[@id="root"]/div/main/div/section[3]/section/section/div/div/section[1]/a').text)
        except:
            address = np.nan
        
        try:
            phone = [str(i.text).strip() for i in driver.find_elements_by_css_selector('p[class="sc-1hez2tp-0 fanwIZ"]')]
        except:
            phone = np.nan
            
        try:
            dining_review1 = str(driver.find_element_by_xpath('//*[@id="root"]/div/main/div/section[3]/section/section/div/div/div/section/div[1]/div[2]/div[1]').text).lower()
            if(dining_review1 == 'newly opened'):
                dining_review1 = np.nan
        except:
            dining_review1 = np.nan
            
        try:
            dining_review2 = str(driver.find_element_by_xpath('//*[@id="root"]/div/main/div/section[3]/section/section/div/div/div/section/div[1]/div[1]/div/div/div[1]').text).lower()
            if(dining_review1 == 'newly opened' or dining_review2=='new'):
                dining_review2 = np.nan
        except:
            dining_review2 = np.nan
     
        try:
            delivery_review1 = str(driver.find_element_by_xpath('//*[@id="root"]/div/main/div/section[3]/section/section/div/div/div/section/div[3]/div[2]/div[1]').text).lower()
            if(dining_review1 == 'newly opened'):
                delivery_review1 = np.nan    
        except:
            delivery_review1 = np.nan
            
        try:
            delivery_review2 = str(driver.find_element_by_xpath('//*[@id="root"]/div/main/div/section[3]/section/section/div/div/div/section/div[3]/div[1]/div/div/div[1]').text).lower()
            if(dining_review1 == 'newly opened'):
                delivery_review2 = np.nan
        except:
            delivery_review2 = np.nan
       
        try:
            new = str(driver.find_element_by_xpath('//*[@id="root"]/div/main/div/section[3]/section/section/div/div/div/section/div/div[2]/div[1]').text).lower()
            if(new != 'newly opened'):
                new = 'old'
            else:
                new = 'new'
        except:
            new = np.nan
        
        record = [name, link, address, phone, dining_review1, dining_review2, delivery_review1, delivery_review2, new]
        record = pd.DataFrame(record).T
        record.columns = ['Name','URL','Address','Phone','# Dining Reviews','Dining Review','# Delivery Reviews', 'Delivery Review', 'Recency']
        print(record.shape)
        print(record)
        
        df.append(record)

        print('*'*100)
        
    
    df = pd.concat(df)
    df = df.reset_index(drop=True)
    print(df.head())

    df.to_csv('final1.csv',index=False)

    driver.quit()