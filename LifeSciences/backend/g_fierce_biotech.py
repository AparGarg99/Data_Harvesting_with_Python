import sys
sys.path.append("../")
from packages import *
from utils import open_browser, random_time_delay, setup, convert_date, save_data, filter_by_date


class fierce_biotech:

    # for a given search result page no., extract all websites on the page 
    def get_page_info(self, driver):
        source = driver.page_source
        soup=bs4.BeautifulSoup(source, 'html.parser')
        
        link=[i.get('href') for i in soup.find_all('a')]
        text=[i.text for i in soup.find_all('a')]
        #############################################################
        INDEX_1=[i for i in range(len(text)) if '$' in text[i]]
        #############################################################
        link=[link[i] for i in INDEX_1]
        text=[text[i] for i in INDEX_1]
        
        return link, text
            
    # Scrape links and headlines from first 5 pages of FierceBiotech
    def parse_pages(self, driver, query):
        y, z = [], []

        # setup progress bar
        my_bar = st.progress(0)
        
        if(query==''):
            # iterate through pages
            npages = 5
            for i in range(1,npages+1):
                # open page
                driver.get(f'https://www.fiercebiotech.com/?page={i}')

                # get websites on the page
                link, text = self.get_page_info(driver)

                link = [f'https://www.fiercebiotech.com/{i}' for i in link]

                print('No. of links and text are: ',len(link),len(text))
                print('*'*50)

                y.append(link)
                z.append(text)
                
                # update progress
                my_bar.progress(i/npages)

        else:
            domains = ['fiercebiotech_com']

            # iterate through domains
            for i, domain in enumerate(domains):
                # open page
                driver.get(f'https://www.fiercepharma.com/search-results?fulltext_search={query}&sort_by=field_date_published&domain={domain}')
                random_time_delay()
            
                # Something wrong with the website. Elements are not clickable until we refresh the page.
                driver.refresh()
                random_time_delay()

                # click 1 time on 'See more articles' button at the bottom to get total 20 results
                driver.find_element_by_link_text('See more articles').click()
                random_time_delay()

                # get websites on the page
                link, text = self.get_page_info(driver)

                if(domain=='fiercebiotech_com'):
                    link = [f'https:{i}' for i in link]
                else:
                    link = [f'https://www.fiercepharma.com/{i}' for i in link]

                print('No. of links and text are: ', len(link), len(text))
                print('*'*50)
                
                y.append(link)
                z.append(text)

                # update progress
                my_bar.progress(i+1/len(domains))

        # Normalize features
        y = [j for i in y for j in i]
        z = [j for i in z for j in i]
        
        return driver, y, z
    
    # extract amount from website title (if present)
    def get_feature_from_title(self, z):
        mag_map = {'m':'million', 'mn':'million', 'million':'million', 'millions':'million', 
                    'b':'billion', 'bn':'billion', 'billion':'billion', 'billions':'billion'}
        amount=[]
        mag=[]
        for i,x in enumerate(z):
            x=re.sub('(?<=\d),(?=\d)', '',x) # replace comma b/w integers $2,800 --> $2800
            x=x.replace(". ", " ").replace(", "," ") # Remove all fullstops from string, except if it's between digits
            x=re.sub('[^A-Za-z0-9$.]+', ' ', x) # remove all special characters except $ and .
            x = x.replace('$ ','$')

            try:
                a=x[x.index('$'):].split()[1], x[x.index('$'):].split()[0][1:]
                amount.append(float(a[1]))
                
            except:
                a=x[x.index('$'):].split()[0][-1], x[x.index('$'):].split()[0][1:-1]
                amount.append(float(a[1]))
                
            mag.append(mag_map.get(a[0].lower(), np.nan))

        currency = ['USD'] * len(z)
        return amount, mag, currency
    
    # Go to each website in DataFrame and scrape Fund type, dates, investors and series type from website body
    def get_features_from_body(self, driver, y):
        investors=[]
        series=[]
        sector=[]
        dates=[]
        sector_list=[' Therapeutics',' Biopharma',' Pharma',' Biotherapeutics',' BioTherapeutics',' Inc',
                     ' Pharmaceuticals',' Bioinformatics','Dx',' Biotics',' Biotechnology',' Diagnostics',' Ltd']
        
        print('Number of articles to parse =',len(y))
        
        # setup progress bar
        my_bar = st.progress(0)

        for j,url in enumerate(y):
            print('Article',j)
            print(url)
            driver.get(url)
            random_time_delay()

            source = driver.page_source
            soup = bs4.BeautifulSoup(source, 'html.parser')       
            a = re.sub('[^A-Za-z0-9.]+', ' ', soup.text)
            a = " ".join(a.split())

            dates.append(soup.find('span',{'class':'date d-block d-md-inline-block'}).text.strip())
            investors.append([i for i in a.split('.') if bool(re.search('investors ',i.lower()))==True])
            series.append([i.lower()[i.lower().find('series'):i.lower().find('series')+8] for i in a.split('.') if i.lower().find('series')!=-1])
            sector.append([a.split(i)[0].split()[-1].strip()+" "+i for i in sector_list if i in a])

            # update progress
            my_bar.progress((j+1)/len(y))
            
        # Normalize investors and series type lists
        for i in range(len(investors)):
            if(sector[i]==[]):
                sector[i]=np.nan
            if(investors[i]==[]):
                investors[i]=np.nan
                
        for i in range(len(series)):
            try:
                series[i] = max(set(series[i]), key = series[i].count)
            except:
                series[i] = np.nan
                
        return driver, investors, series, sector, dates
    

    # Put everything scraped in a dataframe
    def prepare_data(self, url, sector, dates, series, investors, currency, mag, amount):
        # Create DataFrame from scraped features
        df = pd.DataFrame(zip(url, sector, dates, series, investors, currency, mag, amount),
                    columns=['Article URL', 'Name of Fund','Date','Fund Type','Fund Manager','Currency','Magnitude','Amount of Funding'])
        
        # change date format
        df['Date'] = df['Date'].apply(lambda x: " ".join(x.split()[:-1]))
        df['Date'] = df['Date'].map(convert_date)

        # Make values NaN in column "Fund Type" if not list allowed_vals
        allowed_vals=['series b', 'series d', 'series a', 'series c','series e']
        df['Fund Type'][~df['Fund Type'].isin(allowed_vals)] = np.nan

        # Make values NaN in column "Magnitude" if not in list allowed_vals
        allowed_vals = ['million','billion']
        df['Magnitude'][~df['Magnitude'].isin(allowed_vals)] = np.nan
        
        # Make values NaN in column "Amount of Funding" if not a float
        def convert(n):
            try:
                return float(n)
            except:
                return np.nan

        df['Amount of Funding'] = df['Amount of Funding'].map(convert)

        # If the same element exists in multiple rows in 'Name of Fund', then consider it not-useful and remove it
        def remove_common(x):
            try:
                return list(set(x) - common)
            except:
                return x
                
        df['Name of Fund'] = df['Name of Fund'].apply(lambda d: d if isinstance(d, list) else [])
        common = set.intersection(*map(set, df['Name of Fund']))
        df['Name of Fund'] = df['Name of Fund'].map(remove_common)
        
        return df.drop_duplicates(subset=['Article URL'])
    
        
    
    def scrape(self, query, start, end):
        # create all needed directories
        paths = setup()
        
        # open chrome driver/browser
        driver = open_browser()

        # get 'Article Title','URL'
        driver, url, title = self.parse_pages(driver, query)
        #print(url, title)
        print(len(url), len(title))
        print('*'*100)

        # get amount from article title
        amount, mag, currency = self.get_feature_from_title(title)
        #print(amount, mag, currency)
        print(len(amount), len(mag), len(currency))
        print('*'*100)
        
        # scrape Fund type, dates, investors and series type from article body
        driver, investors, series, sector, dates = self.get_features_from_body(driver, url)
        #print(investors, series, sector, dates)
        print(len(investors), len(series), len(sector), len(dates))
        print('*'*100)

        # aggregate all info into a dataframe
        df = self.prepare_data(url, sector, dates, series, investors, currency, mag, amount)
        print(df)
        print('*'*100)
        
        # filter rows by publication date
        df = filter_by_date(df, 'Date', start, end)
        print(df)
        print('*'*100)
        
        # close browser
        driver.quit()

        # save data to excel file
        save_data(filename='g_fierce_biotech.xlsx', path=paths['OUTPUT_DIR'], df=df)
                
        return df