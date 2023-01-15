import sys
sys.path.append("../")
from packages import *
from utils import open_browser, random_time_delay, setup, save_data

class google_finance:
    # open and extract information from comapny's google finance page
    def get_info(self, driver, company):

        # open comapny's google finance page
        url = f'https://www.google.com/search?tbm=fin&q={"+".join(company.strip().split())}'
        driver.get(url)
        random_time_delay()

        # extract page source
        source = driver.page_source
        soup = bs4.BeautifulSoup(source, 'html.parser')

        # get company ticker
        try:
            ticker = driver.current_url.split('/')[-1]
            ticker = ticker.split(':')[0]
        except:
            ticker = np.nan

        # public/non-public flag
        try:
            if('www' in driver.current_url.split(':')[-1]):
                raise
            public_flag = 'public'
        except:
            public_flag = 'non-public'
            
        return ticker, public_flag
    
    def scrape(self, company_list):
        # create all needed directories
        paths = setup()

        # open chrome driver/browser
        driver = open_browser()

        # Initialize list
        df = []

        # setup progress bar
        my_bar = st.progress(0)

        # iterate through companies in given company list
        for count, company in enumerate(company_list):
            
            # open and extract information from comapny's google finance page
            ticker, public_flag = self.get_info(driver, company)

            # put extacted info in a row
            row = [company, ticker, public_flag]

            # add row to the dataframe table
            df.append(row)

            # update/increment progress bar
            my_bar.progress((count+1)/len(company_list))

            # wait after loop completion
            random_time_delay()

        # convert list to dataframe
        df = pd.DataFrame(df, columns=['company', 'ticker','public_flag'])

        # close browser
        driver.quit() 

        # save data to excel file
        save_data(filename='a_google_finance.xlsx', path=paths['OUTPUT_DIR'], df=df.sort_values(by=['public_flag'], ascending=False))

        return df