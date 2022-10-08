from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import bs4
import pandas as pd
import time
import undetected_chromedriver as uc
import argparse
import random
import urllib3
import warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")


def random_time_delay():
    time.sleep(random.uniform(60,80))


def open_driver(): 
    ua = UserAgent()
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument("--mute-audio")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--ignore-certificate-errors')
    #chrome_options.add_argument(f"user-agent={ua['google chrome']}")

    driver = uc.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
    #driver.delete_all_cookies()
    
    return driver


def login(driver, username, password):  
    # go to login page
    driver.get("https://www.instagram.com")
    random_time_delay()

    # Type username
    emailid = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username"))) 
    emailid.send_keys(username)
    random_time_delay()

    # Type password
    passwordid = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "password")))
    passwordid.send_keys(password)
    random_time_delay()

    # Click on the signin button
    signinButton = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')))
    ActionChains(driver).move_to_element(signinButton).click().perform()
    random_time_delay()
    
    return driver


def filter_chats(driver):
    all_chats = driver.find_elements_by_css_selector('div[class=" _ab8s _ab8w  _ab94 _ab99 _ab9f _ab9m _ab9p _abcm"]')
    print('\tTotal Chats:',len(all_chats)) 
    result = list(filter(lambda i: i.find_elements_by_css_selector('div[class="_ab8w  _ab94 _ab97 _ab9h _ab9k _ab9p  _abb0 _abcm"]')==[], all_chats)) # unseen blue dot
    print('\tSelected Chats:', len(result))
    return result



def get_last_msg(driver, chats, word_count):
    df = []
    
    for i in chats:
        try:
            # Click on the chat
            i.click()
            random_time_delay()

            # Get the username
            user = driver.find_element_by_css_selector('button[class="_acan _acao _acaq _acat"]').text.split('\n')[0].strip()
            
            # Get last message
            source = driver.page_source
            soup = bs4.BeautifulSoup(source, 'html.parser')
            msgs = [i.text for i in soup.find_all('div',{'class':'_aacl _aaco _aacu _aacx _aad6 _aade'})]
            last_msg = msgs[-1]

            # Go back to the main inbox page
            driver.back()
            random_time_delay()

            row = [user,last_msg]

            if(len(last_msg.split())>word_count):
                print(row)
                df.append(row)


        except Exception as e:
            print(e)
            #print('Non-text modal encountered')
            pass

        
    df2 = pd.DataFrame(df,columns = ['User','Last Message'])
    
    return df2

if __name__ ==  '__main__':
    
    ########################################## Get user input ##########################################
    parser = argparse.ArgumentParser("Scrape last message in DM left unreplied by other person.")
    parser.add_argument('-f', '--filepath', type=str, default='test_input_csv_files/Msg_input.csv', help='Input file path containing channel login credentials to inbox messages (default = "test_input_csv_files/Msg_input.csv")')
    parser.add_argument('-wc', '--wordcount', type=int, default=2, help='Filter for number of words in last message (default = 2)')

    args = parser.parse_args()

    credentials = pd.read_csv(args.filepath)

    ########################################## Scrape ##########################################
    df3 = []

    for i in range(len(credentials)):
        print('Processing Channel:', i+1, '/', len(credentials))
        
        try:
            # open browser
            driver = open_driver()
            
            # get instagram login credentials
            username = credentials.iloc[i,0]
            password = credentials.iloc[i,1]

            # login
            driver = login(driver, username, password)

            # open inbox
            driver.get('https://www.instagram.com/direct/inbox/')

            # scrolling
            print('Manually Scroll...')
            time.sleep(3*60)

            # Get seen chats only
            chats = filter_chats(driver)

            # Get last message in the seen chats
            df = get_last_msg(driver, chats, args.wordcount)
            df['Login Username'] = username
            print(df.head(5).to_string())

            df3.append(df)

            # close browser
            driver.quit()
            random_time_delay()

            print('*'*100)
            
        except Exception as e:
            print(e)
            pass


    df4 = pd.concat(df3).reset_index(drop=True)
    print(df4.head())

    df4.to_csv('test_output_csv_files/Msg_output.csv',index=False)


