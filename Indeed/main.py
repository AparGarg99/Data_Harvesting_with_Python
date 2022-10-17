########################################## Import Dependencies ##########################################
from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import time
import random
import urllib3
import warnings
import bs4
import pandas as pd
from tqdm import tqdm
import os
import glob
import numpy as np
import bs4
import re
import argparse
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

########################################## Scraping Functions ##########################################
def random_time_delay():
    time.sleep(random.uniform(15,20))

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


def scrape_main_page(url, page_no, checkpoints_dir):
    driver.get(url)

    source = driver.page_source
    soup = bs4.BeautifulSoup(source, 'html.parser')

    posts = soup.find('ul',{'class':'jobsearch-ResultsList css-0'}).find_all('li')

    df = []
    for post in posts:
        try:
            new_flag = post.find('div',{'class':'new css-ud6i3y eu4oa1w0'}).text.strip()
        except:
            new_flag = np.nan

        try:
            title = post.find('a', {'class': re.compile(r'JobTitle')}).text.strip()
        except:
            title = np.nan

        try:
            job_url = post.find('a', {'class': re.compile(r'JobTitle')})['href']
            job_url = 'https://sg.indeed.com' + job_url
        except:
            job_url = np.nan

        try:
            company_name = post.find('span',{'class':'companyName'}).text.strip()
        except:
            company_name = np.nan

        try:
            company_url = post.find('span',{'class':'companyName'}).find('a')['href']
            company_url = 'https://sg.indeed.com' + company_url
        except:
            company_url = np.nan

        try:
            tags = post.find_all('div',{'class':'metadata'})
            tags = list(map(lambda x:x.text.strip(), tags))
        except:
            tags = np.nan

        try:
            job_snippet = post.find('div',{'class':'job-snippet'}).text.strip()
        except:
            job_snippet = np.nan

        try:
            date = post.find('span',{'class':'date'}).text
            date = date.split('Posted')[-1].strip()
        except:
            date = np.nan

        row = [title, job_url, company_name, company_url, tags, job_snippet, date, new_flag]

        df.append(row)
        
    df = pd.DataFrame(df,columns=['job_title', 'job_url', 'company_name', 'company_url', 'job_tags', 'job_snippet', 'job_post_date', 'new_job_post_flag'])
     
    df.to_csv(f'{checkpoints_dir}/page{page_no}.csv',index=False)
    
    next_page_url = 'https://sg.indeed.com' + soup.find('a',{'aria-label':'Next Page'})['href']

    return next_page_url

def scrape_application_page(url):
    try:
        driver.get(url)
        random_time_delay()
        source = driver.page_source
        soup = bs4.BeautifulSoup(source, 'html.parser')
        
        # If 'Apply on company site' is not in the page source, then it is definitely 'Apply Now'
        if(("Apply on company site" in soup.text)==False):
            return 'Apply Now'
        
        # If 'Apply on company site' is in the page source, then it is definitely not 'Apply Now' and has a application page url
        else:
            apply_url = ''
            for i in soup.find_all('a'):
                try:
                    if('applystart' in i['href']):
                        apply_url = i['href']
                        break
                except:
                    pass
            # Check if application page url is mycareersfuture
            if(apply_url!=''):
                driver.get(apply_url)
                random_time_delay()
                if('mycareersfuture' in driver.current_url):
                    return 'mycareersfuture'
                else:  
                    return apply_url
            else:
                return np.nan
    except:
        return np.nan

if __name__ ==  '__main__':
    ########################################## Get user input ##########################################
    parser = argparse.ArgumentParser("Scrape job listings from Indeed")
    parser.add_argument('-m', '--mode', type=str, choices=['url','query'], default='url', help='Want to give url as input or query? (default = url)')
    parser.add_argument('-f', '--filepath', type=str, default='test_input_csv_files/input.csv', help='Input file path containing channel links to get users of tagged posts (default = "test_input_csv_files/input.csv")')
    parser.add_argument('-s', '--savemode', type=str, choices=['imp','all'], default='imp', help='Save all scraped columns in final csv or just important columns? (default = imp)')

    args = parser.parse_args()
    
    input_file = pd.read_csv(args.filepath)
    if(args.mode=='url'):
        input_file = input_file[['url']].dropna()
    elif(args.mode=='query'):
        input_file = input_file[['query','salary']].dropna()
    
    print('########################################## Scrape ##########################################')
    driver = open_browser()
     
    for i in tqdm(range(len(input_file))):
        if(args.mode=='url'):
            url = input_file['url'][i]
        elif(args.mode=='query'):
            query = input_file['query'][i]
            salary = input_file['salary'][i]
            url = f"https://sg.indeed.com/jobs?q={query.replace(' ','+')}+%24{7*12}%2C000&l=Singapore&sc=0kf%3Aattr%28EXSNN%29jt%28fulltime%29%3B"
        
        # Create checkpoints directory
        checkpoints_dir = os.path.join('checkpoints', str(i))
        if not os.path.exists(checkpoints_dir):
            os.makedirs(checkpoints_dir)
            
        # Scrape posts from main page
        end_page_flag = False
        page_no = 0
    
        while(end_page_flag==False):
            try:
                next_page_url = scrape_main_page(url, page_no, checkpoints_dir)
                url = next_page_url
                page_no = page_no+1
                random_time_delay()
            except Exception as e:
                #print(e)
                print('Last Page:',page_no)
                end_page_flag = True
                
    print('########################################## Data Preparation ##########################################')
    final_dir = f'saved_files_{os.path.basename(args.filepath)[:-4]}'
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)
        
    input_file.to_csv(f'{final_dir}/new_input_file.csv',index=False)
            
    for i in tqdm(range(len(input_file))):
        # Read csv files in checkpoints directory
        checkpoints_dir = os.path.join('checkpoints', str(i))
        all_files = glob.glob(os.path.join(checkpoints_dir, "*.csv"))
        final = [pd.read_csv(i) for i in all_files]
        final = pd.concat(final,ignore_index=True)
        
        # Preprocess
        final = final.dropna(subset=['job_title'])
        final = final.drop_duplicates(subset=['company_name','job_title'],ignore_index=True)
        final['job_post_days'] = final['job_post_date'].str.extract('(\d+)')
        final['job_post_days'] = final['job_post_days'].fillna('0').astype(int)
        final['apply_now'] = final['job_url'].map(scrape_application_page)
        final = final[final['apply_now']!='mycareersfuture'] # mycareersfuture only for Singapore PR/Citizen
        final = final.sort_values(by=['job_post_days'],ignore_index=True)
        
        # re-arrange columns
        if(args.savemode=='imp'):
            final = final[['apply_now', 'job_post_days', 'company_name', 'job_title', 'job_url']]
        elif(args.savemode=='all'):
            final = final[['apply_now', 'new_job_post_flag', 'job_post_days', 'company_name', 'company_url', 'job_title', 'job_tags', 'job_snippet', 'job_url']]
        
        # Save dataframe as csv file
        final.to_csv(f'{final_dir}/{str(i)}.csv',index=False)
        
    driver.quit()
