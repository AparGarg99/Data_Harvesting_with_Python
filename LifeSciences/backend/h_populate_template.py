import sys
sys.path.append("../")
from packages import *
from utils import setup, save_data

class populate_template:
    def prep_sheet1(self, patent_df, trials_df):
        # merge patents and trials
        df = pd.merge(patent_df, trials_df, left_on='Company Name/Assignee', right_on='Company Name')
        df = df.drop(['Company Name'],axis=1)
        df = df.drop_duplicates()
        df = df[['Company Name/Assignee', 'Patent No.', 'Title', 'Year Filed',
               'Inventors/Authors', 'Clinical Trial Identifier',
               'Title of study', 'Start Date', 'End Date', 'Sponsor Company',
               'Principal Investigator']]
        
        # rename columns
        df.columns=['Company Name','Application No','IP Title','IP Year',
                     'Inventors','Clinical Trial ID','Clinical Title',
                    'Start Date', 'End Date', 'Sponsor', 'Investigator']
        
        # make duplicate rows as nan
        df2 = df.iloc[:,:5]
        dup_index = set(df2.index)-set(df2.drop_duplicates(keep='first').index)
        df2.iloc[list(dup_index),1:] = np.nan
        
        df3 = df.iloc[:,5:]
        df3['a'] = df['Company Name']
        dup_index=set(df3.index)-set(df3.drop_duplicates(keep='first').index)
        df3.iloc[list(dup_index)] = np.nan
        df3 = df3.drop('a',axis=1)
        
        df = pd.concat([df2, df3],axis=1)
        
        # load template
        template = pd.read_excel('Template.xlsx')
        template.columns = template.iloc[0,:]

        # add null columns as per template
        add_columns = set(template.columns)-set(df.columns)
        for i in add_columns:
            df[i] = np.nan

        # rearrange columns as per template
        df = df[template.columns]

        return df
        
    def prep_sheet2(self, df):
        # prepare check file
        y = df.groupby('Company Name').count()[['Application No','Clinical Trial ID']]
        l1, l2 = [],[]
        
        for i in y['Application No']:
            if(i==0):
                l1.append('N')
            else:
                l1.append('Y')
                
        for i in y['Clinical Trial ID']:
            if(i==0):
                l2.append('N')
            else:
                l2.append('Y')
                
        y['Patent (Y/N)'] = l1
        y['Clinical Trials (Y/N)'] = l2
        y['Company Name'] = y.index
        y = y[['Company Name', 'Patent (Y/N)','Application No','Clinical Trials (Y/N)','Clinical Trial ID']]
        y.columns = ['Company Name', 'Patent (Y/N)','Value','Clinical Trials (Y/N)','Value']
        y = y.sort_values(by=['Patent (Y/N)', 'Clinical Trials (Y/N)'])
        
        ordered_df = []
        for i in y['Company Name']:
            ordered_df.append(df[df['Company Name']==i])
        ordered_df = pd.concat(ordered_df)
        
        return ordered_df, y


    def scrape(self, patent_file, trials_file):
        # create all needed directories
        paths = setup()

        # load data
        patent_df = pd.read_excel(patent_file, engine='openpyxl')
        trials_df = pd.read_excel(trials_file, engine='openpyxl')

        # prepare Harvest sheet
        df1 = self.prep_sheet1(patent_df, trials_df)

        # prepare Check sheet
        df1, df2 = self.prep_sheet2(df1)

        # save to excel
        save_data(filename='h_populate_template.xlsx', path=paths['OUTPUT_DIR'], df=df1, df2=df2)