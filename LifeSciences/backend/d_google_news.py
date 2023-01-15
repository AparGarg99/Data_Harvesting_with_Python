import sys
sys.path.append("../")
from packages import *
from utils import open_browser, random_time_delay, setup, convert_date, save_data, filter_by_date

class google_news:
    # for a given company name search query, for a given search result page no., extract all websites on the page
    def get_page_info(self, driver, company, query, page_no):

        # open the page
        # #"<COMPANY NAME> raises financing"
        driver.get(f'https://www.google.com/search?&tbm=nws&q={company} {query}&start={page_no}') 
        random_time_delay()
        
        # extract page source
        source = driver.page_source
        soup = bs4.BeautifulSoup(source, 'html.parser')
        
        # get info
        sections = soup.find_all('div',{'class':'SoaBEf'})

        link, text, date, website =  [],[],[],[]
        for section in sections:
            website += [i.text for i in section.find_all('div',{'class':'CEMjEf NUnG9d'})]
            link += [i.get('href') for i in section.find_all('a',{'class':'WlydOe'})]
            text += [i.text for i in section.find_all('div',{'role':'heading'})]
            date += [i.text for i in section.find_all('div',{'class':'OSrXXb ZE0LJd YsWzw'})]

        INDEX_1 = [i for i in range(len(text)) if '$' in text[i]]
        link = [link[i] for i in INDEX_1]
        text = [text[i] for i in INDEX_1]
        date = [date[i] for i in INDEX_1]
        website = [website[i] for i in INDEX_1]
        
        return link, text, date, website
    
    
    # extract websites for all company name search queries, for first 5 page no.
    def get_info(self, driver, company_list, query):
        x,k,y,z,m=[],[],[],[],[]

        # setup progress bar
        my_bar = st.progress(0)

        # iterate through companies in given company list
        for j,company in enumerate(company_list):
            print(j, company)
            try:
                # iterate through first 5 pages of google page results and extract all websites from those pages
                for page_no in range(0,50,10):
                    link, text, date, website = self.get_page_info(driver, company, query, page_no)
                    print('Page No.',int(str(page_no)[0])+1)
                    print('No. of links and text are: ',len(link),len(text),len(date),len(website))
                    x.append(date)
                    y.append(link)
                    z.append(text)
                    k.append(website)
                    m.append([company for i in range(len(website))])
                    print('*'*50)
                    #print(x, k, y, z, m)
            except Exception as e:
                print(e)
                pass
            print('*'*100)

            # update/increment progress bar
            my_bar.progress((j+1)/len(company_list))
            
                           
        # Normalize features
        x=[j for i in x for j in i]
        k=[j for i in k for j in i]
        y=[j for i in y for j in i]
        z=[j for i in z for j in i]
        m=[j for i in m for j in i]

        return x,k,y,z,m
    
    # extract amount from website title (if present)
    def scrape_amount(self, z):
        key=['million','billion','millions','billions','trillion','trillions']
        amount=[]
        for x in z:
            try:
                if(x[x.index('$'):].split()[1].lower() in key):
                    amount.append(x[x.index('$'):].split()[0]+' '+x[x.index('$'):].split()[1])
                else:
                    amount.append(x[x.index('$'):].split()[0])
            except:
                amount.append(x[x.index('$'):].split()[0])
        return amount
    
    
    # Put everything scraped in a dataframe
    def prepare_data(self, m, x, z, y, amount):
        # Create DataFrame from scraped features
        df = pd.DataFrame(zip(m,x,z,y,amount), columns=['Company Name','Date','Article Title','URL','Amount'])

        # Keep only those rows where Company Name is in Article Title
        df['temp']=df['Company Name'].apply(lambda x: x.split()[0])
        
        df['C'] = df.apply(lambda x: str(x['temp']) in str(x['Article Title']), axis=1)
        
        df=df.loc[df['C']==True].drop(['temp','C'],axis=1)

        return df
    
    # Go to each website in DataFrame and scrape investors and series type from website body
    def get_investors_and_series(self, driver, df):
        investors=[]
        series=[]
        for j,url in enumerate(df['URL']):
            print('Article',j)
            driver.get(url)
            random_time_delay()
            source = driver.page_source
            soup=bs4.BeautifulSoup(source, 'html.parser')
            for script in soup(["script", "style"]):
                script.extract()    
            a = soup.get_text()
            a=" ".join(a.split())
            a=re.sub('[^A-Za-z0-9.]+', ' ', a)
            investors.append([i for i in a.split('.') if bool(re.search('investors ',i.lower()))==True])
            series.append([i.lower()[i.lower().find('series'):i.lower().find('series')+8] for i in a.split('.') if i.lower().find('series')!=-1])
        
        
        # Normalize investors and series type lists
        for i in range(len(investors)):
            if(investors[i]==[]):
                investors[i]=np.nan
                
        for i in range(len(series)):
            try:
                series[i] = max(set(series[i]), key = series[i].count)
            except:
                series[i] = np.nan
        
        # Save lists to DataFrame
        df['Series Type'] = series
        df['Investors'] = investors
        
        return df
        
        
    # Some Data Manipulation in dataframe
    def data_cleaning(self, df):
        # Make all values NaN in column "Series Type", except those which are in list allowed_vals
        allowed_vals = ['series b', 'series d', 'series a', 'series c','series e']
        df['Series Type'][~df['Series Type'].isin(allowed_vals)] = np.nan

        # Arranging Columns of DataFrame
        df = df[['Company Name', 'Date', 'Article Title', 'URL', 'Series Type', 'Amount', 'Investors']]
        
        # change date format
        df['Date'] = df['Date'].map(convert_date)
        
        return df
    
    
    # Some more Data Manipulation in dataframe
    def final_prep_sheet1(self, company_list, df):
        # Add not-scraped companies to DataFrame
        not_scraped = list(set(company_list)-set(df['Company Name'].unique()))
        if(len(not_scraped)!=0):
            s2 = [[i, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan] for i in not_scraped]
            s2 = pd.DataFrame(s2)
            s2.columns = df.columns
            df = pd.concat([df, s2], ignore_index=True)
        
        # sort rows by 'Company Name','Date'
        temp = df.copy()
        temp['Date'] = pd.to_datetime(temp['Date'])
        temp = temp.sort_values(by=['Company Name','Date']) 
        df = df.loc[temp.index].reset_index(drop=True)
        
        return df, not_scraped
    
    # prepare patent check sheet
    def prep_sheet2(self, df, not_scraped):
        df2 = df.groupby(['Company Name']).size().reset_index(name='Value')
        df2['Value'] = df2.apply(lambda x: 0 if x['Company Name'] in not_scraped else x['Value'] , axis=1)
        df2['Financing Rounds (Y/N)'] = df2['Value'].apply(lambda x: 'Y' if x>0 else 'N')
        df2 = df2.reset_index(drop=True)
        return df2
          

    def scrape(self, company_list, query, start, end):
        # create all needed directories
        paths = setup()
        
        # open chrome driver/browser
        driver = open_browser()

        # get 'Company Name','Date','Article Title','URL','Amount'
        x, k, y, z, m = self.get_info(driver, company_list, query)
        #print(x, k, y, z, m)

        # Get amount from title
        amount = self.scrape_amount(z)
        #print(amount)

        # aggregate all info into a dataframe
        df = self.prepare_data(m, x, z, y, amount)
        print(df)
        print(df.columns)
        print('*'*100)
        
        # add 2 more columns 'Series Type', 'Investors'
        df = self.get_investors_and_series(driver, df)
        print(df)
        print(df.columns)
        print('*'*100)
        
        # clean the dataframe
        df = self.data_cleaning(df)
        print(df)
        print('*'*100)
        
        # filter rows by date
        df = filter_by_date(df, 'Date', start, end)
        print(df)
        print('*'*100)
        
        # Add not-scraped companies to DataFrame
        df, not_scraped = self.final_prep_sheet1(company_list, df)
        print(df)
        print('*'*100)
        
        # prepare trials check sheet
        df2 = self.prep_sheet2(df, not_scraped)

        # close browser
        driver.quit()

        # save data to excel file
        save_data(filename='d_google_news.xlsx', path=paths['OUTPUT_DIR'], df=df, df2=df2)
        
        return df, df2