import sys
sys.path.append("../")
from packages import *
from utils import open_browser, random_time_delay, setup, convert_date, save_data, filter_by_date

class google_patent:
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
                # form url request
                url = f"https://patents.google.com/xhr/query?url=assignee%3D{'%2B'.join(company.split())}%26oq%3D{'%2B'.join(company.split())}&exp=&download=true"

                # download csv
                webbrowser.open(url)

                # wait
                random_time_delay()

                # read csv from downloads
                file = glob.glob(os.path.join(paths['DOWNLOADS_DIR'], "*.csv"))[0]

                # rename csv
                os.rename(file, os.path.join(paths['DOWNLOADS_DIR'], f'{company}.csv'))

                # copy csv to req. folder
                shutil.copy(os.path.join(paths['DOWNLOADS_DIR'], f'{company}.csv'), paths['PATENT_DIR'])

                # delete csv from downloads
                self.delete(paths['DOWNLOADS_DIR'])


            except Exception as e:
                #print(e)
                pass

            # update/increment progress bar
            my_bar.progress((j+1)/len(company_list))

    # put all downloaded data into one single csv file
    def aggregate_data(self, paths):
        # read all csv files in subdirectory "Patent files"
        df = glob.glob(os.path.join(paths['PATENT_DIR'], "*.csv"))

        # concatenate all csv files present in "Patent files"
        df = [pd.read_csv(f,header=1) for f in df]
        df = pd.concat(df, ignore_index=True)
        df = df.astype(str)
        df = df[['id', 'title', 'publication date', 'assignee', 'inventor/author']]
        df = df.reset_index(drop=True)

        return df
    
    # google patents doesn't give 100% accurate resutls. 
    # sometimes assignee name in results doesn't match with input company name
    # this function removes those inaccurate rows
    def row_manipulation(self, df, company_list):
        df2 = []
        s = df['assignee'].apply(lambda x: re.sub(r'[^\w\s]', '', x.lower()))
        for company in company_list:
            k = s[s.str.contains(re.sub(r'[^\w\s]', '', company.lower()))].index
            if(list(k)!=[]):
                temp = df.loc[k]
                temp['assignee'] = company
                df2.append(temp)
        df2 = pd.concat(df2)
        df2 = df2.reset_index(drop=True)
        
        return df2
    
        
    # Feature Engineering, Feature Transformation, Feature Selection, Feature Renaming in dataframe
    def column_manipulation(self, df2):
        # Feature Transformation of date
        df2['publication date'] = df2['publication date'].map(convert_date)
        
         # Feature Engineering "Year Filed" from "publication date"
        df2['Year Filed'] = pd.to_datetime(df2['publication date']).apply(lambda x: x.strftime("%Y"))

        # selecting required columns
        df2 = df2[['assignee', 'id', 'title', 'publication date', 'Year Filed', 'inventor/author']]

        # renaming columns
        df2.columns=['Company Name/Assignee','Patent No.','Title','Publication Date','Year Filed','Inventors/Authors']
        df2 = df2.replace('nan',np.nan)
        df2 = df2.reset_index(drop=True)

        return df2
        

    # Some more Data Manipulation in dataframe
    def final_prep_sheet1(self, company_list, df2):
        # Add not-scraped companies to DataFrame
        not_scraped = list(set(company_list) - set(df2['Company Name/Assignee'].unique()))
        if(len(not_scraped)!=0):
            s2 = [[i, np.nan, np.nan, np.nan, np.nan, np.nan] for i in not_scraped]
            s2 = pd.DataFrame(s2)
            s2.columns = df2.columns
            df2 = pd.concat([df2, s2], ignore_index=True)
        
        # sort rows by 'Company Name/Assignee','Publication Date'
        temp = df2.copy()
        temp['Publication Date'] = pd.to_datetime(temp['Publication Date'])
        temp = temp.sort_values(by=['Company Name/Assignee','Publication Date']) 
        df2 = df2.loc[temp.index].reset_index(drop=True)
        
        return df2, not_scraped
    
    # prepare patent check sheet
    def prep_sheet2(self, df2, not_scraped):
        df3 = df2.groupby(['Company Name/Assignee']).size().reset_index(name='Value')
        df3['Value'] = df3.apply(lambda x: 0 if x['Company Name/Assignee'] in not_scraped else x['Value'] , axis=1)
        df3['Patent (Y/N)'] = df3['Value'].apply(lambda x: 'Y' if x>0 else 'N')
        df3 = df3.reset_index(drop=True)
        
        return df3
    
        
    def scrape(self, company_list, start, end):
        # create all needed directories
        paths = setup()

        # detete csv files from "Downloads" directory (if any)
        self.delete(paths['DOWNLOADS_DIR'])

        # detete csv files from output subdirectory (if any)
        self.delete(paths['PATENT_DIR'])

        # download csv containing list of patents for every company
        self.download_data(paths, company_list)

        # Combine all patent files
        df = self.aggregate_data(paths)
        print(df)
        print('*'*100)

        # filter output based on "assignee"
        df2 = self.row_manipulation(df, company_list)
        print(df2)
        print('*'*100)

        # Feature Engineering, Feature Transformation, Feature Selection, Feature Renaming
        df2 = self.column_manipulation(df2)
        print(df2)
        print('*'*100)

        # selet rows that fall between input start and end publication date
        df2 = filter_by_date(df2, 'Publication Date', start, end)
        print(df2)
        print('*'*100)

        # Add not-scraped companies to DataFrame
        df2, not_scraped = self.final_prep_sheet1(company_list, df2)
        print(df2)
        print('*'*100)

        # prepare patent check sheet
        df3 = self.prep_sheet2(df2, not_scraped)
        print(df3)
        print('*'*100)

        # save data to excel file
        save_data(filename='b_google_patent.xlsx', path=paths['OUTPUT_DIR'], df=df2, df2=df3)
        
        return df2, df3