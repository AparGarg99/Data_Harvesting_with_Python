from webdriver_manager.chrome import ChromeDriverManager
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import time
import bs4
import pickle
import urllib3
import warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")

if __name__ ==  '__main__':
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

    ########################################## Open the page ##########################################
    driver.get('https://www.zomato.com/india')
    time.sleep(10)

    ########################################## Scrape cities ##########################################
    source = driver.page_source
    soup = bs4.BeautifulSoup(source, 'html.parser')

    div = soup.find('div',{'class':'sc-bke1zw-0 fIuLDK'})

    cities = []
    for i in div.find_all('a'):
        try:
            cities.append(i['href'].split('/')[-1])
        except:
            pass

    cities = sorted(cities)

    d = {}
    for i in range(len(cities)):
        d[i] = cities[i]

    print(d)

    # with open('india_cities.pkl', 'wb') as f:
    #     pickle.dump(d, f, protocol=pickle.HIGHEST_PROTOCOL)