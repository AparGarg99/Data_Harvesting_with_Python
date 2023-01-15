import sys
sys.path.append("../")
from packages import *
from utils import open_browser, random_time_delay, setup, convert_date, save_data, filter_by_date

class clinical_trial:

    # delete all csv files in a given directory
    def delete(self, directory):
        filelist = [ f for f in os.listdir(directory) if f.endswith(".csv")]
        for f in filelist:
            os.remove(os.path.join(directory, f))
                    
    # download patents for all companies in company list
    def download_data(self, paths, company_list):
        # setup progress bar
        my_bar = st.progress(0)

        # iterate through companies in given company list
        for j, company in enumerate(company_list):
            try:
                url = f"https://clinicaltrials.gov/ct2/results/download_fields?cond=&term={'+'.join(company.split())}&type=&down_fmt=csv&down_flds=all&rslt=&age_v=&gndr=&intr=&titles=&outc=&spons=&lead=&id=&cntry=&state=&city=&dist=&locn=&fund=2&rsub=&strd_s=&strd_e=&prcd_s=&prcd_e=&sfpd_s=&sfpd_e=&rfpd_s=&rfpd_e=&lupd_s=&lupd_e=&sort="
                df = pd.read_csv(url)
                df = df[['First Posted','NCT Number','Title','Start Date','Completion Date','Sponsor/Collaborators']]
                df['Company Name'] = company
                df.to_csv(os.path.join(paths['TRIALS_DIR'], f'{company}.csv'),index=False)
                random_time_delay()
            except Exception as e:
                print(e)
                pass

            # update/increment progress bar
            my_bar.progress((j+1)/len(company_list))

    # put all downloaded data into one single csv file
    def aggregate_data(self, paths):
        all_files = glob.glob(os.path.join(paths['TRIALS_DIR'], "*.csv"))

        df = pd.concat([pd.read_csv(i) for i in all_files])

        df = df.reset_index(drop=True)
        
        return df


    # Feature Engineering, Feature Transformation, Feature Selection, Feature Renaming in dataframe
    def column_manipulation(self, df):   
        df['Principal Investigator'] = '-' 

        df = df[['Company Name','NCT Number','Title', 'Start Date', 'Completion Date','Sponsor/Collaborators','Principal Investigator']]

        df.columns=['Company Name', 'Clinical Trial Identifier', 'Title of study', 'Start Date', 'End Date', 'Sponsor Company', 'Principal Investigator']

        df['Start Date'] = df['Start Date'].map(convert_date)
        
        df['End Date'] = df['End Date'].map(convert_date)
        
        df = df.reset_index(drop=True)
        
        return df
        
    # website doesn't give 100% accurate resutls. 
    # sometimes Sponsor Company name in results doesn't match with input company name
    # this function removes those inaccurate rows
    def row_manipulation(self, df):
        df['filter'] = df.apply(lambda x: str(x['Company Name']) in str(x['Sponsor Company']), axis=1)

        df = df[df['filter']==True]

        df = df.drop('filter',axis=1)
        
        df = df.reset_index(drop=True)
        
        return df
        
        
    # extract principal investigator names
    def find_principal_investigator(self, driver, df):
        keywords = ['Study Director:','Principal Investigator:']

        # setup progress bar
        my_bar = st.progress(0)

        for i in range(len(df)):
            url = f"https://clinicaltrials.gov/ct2/show/{df['Clinical Trial Identifier'][i]}"
            driver.get(url)
            source = driver.page_source
            soup = bs4.BeautifulSoup(source, 'html.parser')  
            try:
                txt = ' '.join([j.text for j in soup.find_all('table',{'class':'ct-layout_table tr-indent2'})])
                for j in keywords:
                    try:
                        df['Principal Investigator'][i] = txt.split(j)[1].strip()
                        break
                    except:
                        pass        
            except Exception as e:
                #print(e)
                pass

            # update/increment progress bar
            my_bar.progress((i+1)/len(df))

            random_time_delay()
                
        df = df.reset_index(drop=True)
                
        return df
    
    
    # Some more Data Manipulation in dataframe
    def final_prep_sheet1(self, company_list, df):
        # Add not-scraped companies to DataFrame
        not_scraped = list(set(company_list)-set(df['Company Name'].unique()))
        if(len(not_scraped)!=0):
            s2 = [[i,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan] for i in not_scraped]
            s2 = pd.DataFrame(s2)
            s2.columns = df.columns
            df = pd.concat([df, s2], ignore_index=True)
        
        # sort rows by 'Company Name','Start Date'
        temp = df.copy()
        temp['Start Date'] = pd.to_datetime(temp['Start Date'])
        temp = temp.sort_values(by=['Company Name','Start Date']) 
        df = df.loc[temp.index].reset_index(drop=True)
        
        return df, not_scraped
    
    # prepare clinical trial check sheet
    def prep_sheet2(self, df, not_scraped):
        df2 = df.groupby(['Company Name']).size().reset_index(name='Value')
        df2['Value'] = df2.apply(lambda x: 0 if x['Company Name'] in not_scraped else x['Value'] , axis=1)
        df2['Clinical Trials (Y/N)'] = df2['Value'].apply(lambda x: 'Y' if x>0 else 'N')
        df2 = df2.reset_index(drop=True)
        return df2
          
    def scrape(self, company_list, start, end):
        # create all needed directories
        paths = setup()

        # open chrome driver/browser
        driver = open_browser()

        # detete csv files from "Downloads" directory (if any)
        self.delete(paths['DOWNLOADS_DIR'])

        # detete csv files from output subdirectory (if any)
        self.delete(paths['TRIALS_DIR'])

        # download csv containing list of patents for every company
        self.download_data(paths, company_list)

        # Combine all patent files
        df = self.aggregate_data(paths)
        print(df)
        print('*'*100)

        # Feature Engineering, Feature Transformation, Feature Selection, Feature Renaming
        df = self.column_manipulation(df)
        print(df)
        print('*'*100)
        
        # filter output based on "assignee"
        df = self.row_manipulation(df)
        print(df)
        print('*'*100)

        # get principle investigator
        df = self.find_principal_investigator(driver, df)
        print(df)
        print('*'*100)

        # filter rows by publication date
        df = filter_by_date(df, 'Start Date', start, end)
        print(df)
        print('*'*100)
        
        # Add not-scraped companies to DataFrame
        df, not_scraped = self.final_prep_sheet1(company_list, df)
        print(df)
        print('*'*100)

        # prepare clinical trial check sheet
        df2 = self.prep_sheet2(df, not_scraped)
        print(df2)
        print('*'*100)

        # close browser
        driver.quit() 

        # save data to excel file
        save_data(filename='c_clinical_trial.xlsx', path=paths['OUTPUT_DIR'], df=df, df2=df2)
        
        return df, df2