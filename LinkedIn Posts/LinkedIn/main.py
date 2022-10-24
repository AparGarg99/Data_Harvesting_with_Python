import os
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import time
import random
import urllib3
import warnings
import bs4
import pandas as pd
from tqdm import tqdm
import glob
import numpy as np
import bs4
import itertools
import nltk
import re
from nltk.corpus import stopwords
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer
import argparse
import re
#os.chdir('C:/Users/aparg/Desktop/LinkedIn')
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
nltk.download('omw-1.4')

directory = 'checkpoints'
if not os.path.exists(directory):
    os.makedirs(directory)

def random_time_delay():
    time.sleep(random.uniform(20,25))


def open_browser():
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
    chrome_options.add_argument(f"user-agent={ua['google chrome']}")
    driver = uc.Chrome(executable_path=ChromeDriverManager().install(), 
                                       options=chrome_options)    
    return driver


def login(driver, email, password):
    driver.get('https://www.linkedin.com/login')
    random_time_delay()
    
    driver.find_element_by_id('username').send_keys(email)
    random_time_delay()
    
    driver.find_element_by_id('password').send_keys(password)
    random_time_delay()
    
    driver.find_element_by_css_selector('button[type="submit"]').click()
    random_time_delay()
    
    return driver


def scroll(driver):
    # set load time
    scroll_pause_time = 8

    # Get screen height
    screen_height = driver.execute_script("return window.screen.height;")  
    i = 1

    while True:
        # scroll one screen height each time
        driver.execute_script(f"window.scrollTo(0, {screen_height}*{i});")
        i += 1

        # Wait to load page
        time.sleep(scroll_pause_time)

        # update scroll height each time after scrolled, as the scroll height can change after we scrolled the page
        scroll_height = driver.execute_script("return document.body.scrollHeight;")

        # Break the loop when the height we need to scroll is larger than the total scroll height
        if (screen_height) * i > scroll_height:
            break
    
    return driver


def get_post_info(full_post): 
    try:
        profile_url = full_post.find('a',{'class':'app-aware-link feed-shared-actor__container-link relative display-flex flex-grow-1'})['href']

        full_post = full_post.text.split('\n')

        full_post = list(filter(lambda x: x.strip()!='',full_post))

        info = np.array(full_post)[[2, 4, 6, 7, 8]].tolist() # Author, Profile Headline, Post Publish Date, Potential Post Body 1, Potential Post Body 2

        info.append(profile_url)
    except:
        info = [np.nan]*6
        
    return info


def get_df(driver):
    # Get page source
    source = driver.page_source
    soup = bs4.BeautifulSoup(source, 'html.parser')
    
    # Get all posts on the page
    full_posts = soup.find_all('div',{'id':re.compile(r'ember')})
    
    # Extract relevant info from all posts
    df = list(map(get_post_info, full_posts))

    # Save data to dataframe
    df = pd.DataFrame(df, columns = ['Author', 'Profile Headline', 'Post Publish Date', 'Potential Post Body 1', 'Potential Post Body 2', 'Profile URL'])
    
    return df.dropna()


def clean_text(body):
    # lowercasing
    body = body.lower()
     
    # tokenization
    body = nltk.word_tokenize(body)
    
    # remove tokens with non-alphabets
    body = [word for word in body if word.isalpha()==True]
    
    # stop-word removal
    body = [word for word in body if word not in stopwords.words('english')]
    
    # lemmatization
    body = [WordNetLemmatizer().lemmatize(word) for word in body]
    
    return " ".join(body)


def filter_df(df):
    # Strip values in all columns
    for i in df.columns:
        df[i] = df[i].apply(lambda x: str(x).strip())
        
    # Remove duplicate records
    df = df.drop_duplicates(subset = ['Author','Post Publish Date'], ignore_index=True)
    print(df.shape)

    # Remove records with short post body length
    l = []
    for row in df.itertuples(index=False):
        if (len(row[-2].split())>10):
            l.append(row[-2])
        elif (len(row[-1].split())>10):
            l.append(row[-1])
        else:
            l.append(np.nan)
    df['Post Body'] = l
    print(df.shape)

    # drop rows with null entries
    df = df.dropna()
    print(df.shape)

    # Remove records in which Post Publish Date does not have 'ago' keyword
    df = df.loc[df['Post Publish Date'].apply(lambda x: 'ago' in x)]
    print(df.shape)
    
    # Remove records in which Post Body does not have the keywords
    df['Clean Post Body'] = df['Post Body'].map(clean_text)
    normalized_keywords = list(map(lambda x: clean_text(x), keywords))
    df = df[df['Clean Post Body'].str.contains("|".join(normalized_keywords))]
    print(df.shape)
    
    # Remove records in which Post Body does not have the job type
    new_df = []
    for job_type in df['Job Type'].unique(): 
        temp = df[df['Job Type']==job_type]
        normalized_job_type = clean_text(job_type)
        temp = temp[temp['Clean Post Body'].str.contains(normalized_job_type)]
        new_df.append(temp)
    new_df = pd.concat(new_df)
    print(new_df.shape)
     
    return new_df

def feature_engineering_df(df):
    df['Email'] = df['Post Body'].apply(lambda x: re.findall('\S+@\S+', str(x)))
    return df

# %%
if __name__ ==  '__main__':
    
    ########################################## Get user input ##########################################
    parser = argparse.ArgumentParser("Scrape job related posts from LinkedIn")
    parser.add_argument('-kf', '--keyword_filepath', type=str, default='test_input_csv_files/keywords.csv', help='Input file path containing search keywords (default = "test_input_csv_files/keywords.csv")')
    parser.add_argument('-jf', '--job_filepath', type=str, default='test_input_csv_files/jobs.csv', help='Input file path containing search job type (default = "test_input_csv_files/jobs.csv")')
    parser.add_argument('-s', '--scroller', choices=['manual','auto'], default='auto', help='Scroll posts manually or automatically (default="auto")')
    parser.add_argument('-e', '--email_id', type=str, required=True, help='email id to login into LinkedIn')
    parser.add_argument('-p', '--password', type=str,  required=True, help='password to login into LinkedIn')

    args = parser.parse_args()
 
    email = args.email_id
    password = args.password
    
    keywords = list(pd.read_csv(args.keyword_filepath,header=None)[0].dropna(axis=0))
    job_types = list(pd.read_csv(args.job_filepath,header=None)[0].dropna(axis=0))
    
    # ########################################## Scrape ##########################################
    # Login
    driver = open_browser()
    driver = login(driver, email, password)
    #time.sleep(2*60) # wait for 2 factor auth
    
    c = 1
    for job_type in job_types:
        search_queries = list(itertools.product(keywords, [job_type]))
        search_queries = list(map(lambda x: " for ".join(x), search_queries))
        
        for search_query in search_queries:
            try:
                print(search_query)

                # Go to LinkedIn page
                driver.get(f'https://www.linkedin.com/search/results/content/?keywords={search_query}')
                random_time_delay()

                # Infinite scrolling
                if(args.scroller=='auto'):
                    driver = scroll(driver)
                    random_time_delay()

                elif(args.scroller=='manual'):
                    print('Manually Scroll...')
                    time.sleep(5*60)

                # Prepare dataframe
                df = get_df(driver)
                
                # Save dataframe to checkpoints folder
                if(len(df)!=0):
                    df.insert(0, 'Job Type', job_type)
                    df.insert(0, 'Search Query', search_query)
                    print(df)
                    df.to_csv(f'{directory}/{c}_{search_query}.csv',index=False)
                
            except Exception as e:
                print(e)
                pass
            
            c = c+1
            print('*'*100)
        
    ########################################## Process ##########################################
    csv_files = glob.glob(f'{directory}/*')
    final = [pd.read_csv(i) for i in csv_files]
    final = pd.concat(final, ignore_index=True)
    final = filter_df(final)
    final = feature_engineering_df(final)
    final = final[['Job Type', 'Search Query', 'Author', 'Profile URL', 'Profile Headline', 'Post Publish Date', 'Post Body', 'Email']]
    final = final.sort_values(by=['Job Type', 'Search Query'], ignore_index=True)

    final.to_csv('final.csv',index=False)

    driver.quit()