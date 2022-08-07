from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import pandas as pd
import random
import time
import argparse
import numpy as np
import urllib3
import warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

if __name__ ==  '__main__':

    ########################################## Get user input ##########################################
    parser = argparse.ArgumentParser(description='Automatic posting of review on a restaurant')
    parser.add_argument('-f', '--filepath', type=str, default='auto_comment.csv', help='Input file path containing restaurant links')
    args = parser.parse_args()
    file = args.filepath
    links = list(pd.read_csv(file,header=None)[0].dropna(axis=0))

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
    chrome_options.add_argument(f"user-agent={ua['google chrome']}")
    driver = uc.Chrome(executable_path=ChromeDriverManager().install(), 
                       options=chrome_options)


    ########################################## Open the main page ##########################################
    driver.get('https://www.zomato.com')
    time.sleep(2*60)

    ########################################## Manual login ##########################################

    ###

    ########################################## Give review ##########################################
    for i,link in enumerate(links):
        print(f'Processing {i+1}/{len(links)}')

        # go to link
        driver.get(link+'/reviews')
        time.sleep(30)
    
        # Click on 'Write a Review' button
        driver.find_element_by_xpath('//*[@id="root"]/div/main/div/section[4]/div/div/section[1]/div/section/a/span').click()
        time.sleep(30)
        
        # Give 4 Star
        driver.find_elements_by_css_selector('div[class="sc-1q7bklc-5 kHxpSk"]')[-3].click()
        time.sleep(30)
        
        # Get Suggestion chips of what you liked
        you_liked = ['//*[@id]/section[2]/section/section[2]/section[1]/span[1]',
                     '//*[@id]/section[2]/section/section[2]/section[1]/span[2]',
                     '//*[@id]/section[2]/section/section[2]/section[1]/span[3]',
                     '//*[@id]/section[2]/section/section[2]/section[1]/span[4]',
                     '//*[@id]/section[2]/section/section[2]/section[1]/span[5]',
                     '//*[@id]/section[2]/section/section[2]/section[1]/span[6]']

        index2 = random.randint(0,len(you_liked)-1)

        element2 = driver.find_element_by_xpath(you_liked[index2])

        
        # Write the review
        review_text = [f"I really liked the {element2.text}. Thank you for the wonderful experience. I recommend it to everyone! I would like to come back here again and again."]
        
        index3 = random.randint(0,len(review_text)-1)

        element3 = review_text[index3]

        print(element3)
        
        driver.find_element_by_xpath('//*[@id]/section[2]/section/section[2]/section[4]/section/section/textarea').send_keys(element3)
        time.sleep(30)
        
        # Click on 'Add Review' button
        driver.find_element_by_xpath('//*[@id]/section[2]/section/section[3]/button/span/span').click()
        time.sleep(30)

        print('*'*100)

    driver.quit()