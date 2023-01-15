import sys
sys.path.append("../")
from packages import *

# open chrome browser
def open_browser():
        chrome_options = uc.ChromeOptions()
        chrome_options.add_argument("--window-size=1920,1080")
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument('--disable-notifications')
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("--start-maximized")
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--ignore-certificate-errors')
        driver = uc.Chrome(executable_path=ChromeDriverManager().install(), options=chrome_options)
        return driver


# random time delay between requests (anti-blocking technique)
def random_time_delay():
        time.sleep(random.uniform(15,25))


# define and creare directory structure
def setup(): 
        today = date.today()
        paths = {
                'OUTPUT_DIR': f'output_{today}',
                'PATENT_DIR': os.path.join(f'output_{today}', 'patent files'),
                'TRIALS_DIR': os.path.join(f'output_{today}', 'trials files'),
                'DOWNLOADS_DIR': str(Path.home() / "Downloads")
                }
        
        # create directory structure
        for path in list(paths.values())[:-1]:
            if not os.path.exists(path):
                os.makedirs(path)
                
        return paths
        

# the dates in results do not follow one consistent format.
# this function brings all dates in one single format i.e. DD/MM/YYYY
def convert_date(x):
    try:
        if('ago' not in x):
            if('-' in x):
                return datetime.strptime(x, '%Y-%m-%d').strftime("%d/%m/%Y")
            elif(',' in x):
                try:
                    return datetime.strptime(x, "%B %d, %Y").strftime("%d/%m/%Y")
                except:
                    return datetime.strptime(x, "%b %d, %Y").strftime("%d/%m/%Y")
            elif('/' in x):
                return datetime.strptime(x, '%d/%m/%Y').strftime("%d/%m/%Y")
            else:
                try:
                    return datetime.strptime(x, '%B %Y').strftime("%d/%m/%Y")
                except:
                    try:
                        return datetime.strptime(x, '%b %Y').strftime("%d/%m/%Y")
                    except:
                        try:
                            return datetime.strptime(x, '%d %b %Y').strftime("%d/%m/%Y")
                        except:
                            return datetime.strptime(x, '%d %B %Y').strftime("%d/%m/%Y")
                            

        elif('ago' in x):
            if('day' in x):
                step = int(x.split('day')[0].strip())
            elif('week' in x):
                step = int(x.split('week')[0].strip())
                step = step*7
            elif('month' in x):
                step = int(x.split('month')[0].strip())
                step = step*30
            elif('year' in x):
                step = int(x.split('year')[0].strip())
                step = step*365

            step = timedelta(days=step)
            d = date.today().strftime("%d/%m/%Y")
            d = datetime.strptime(d, "%d/%m/%Y")
            d = d - step
            return d.strftime("%d/%m/%Y")

    except:
        return x


# save data to excel file
def save_data(filename, path, df, df2=None):
    writer = pd.ExcelWriter(os.path.join(path, filename), engine='xlsxwriter')

    df.to_excel(writer, sheet_name='Harvest',index=False)

    try:
        df2.to_excel(writer, sheet_name='Check',index=False)
    except:
        pass

    writer.save()


# selet rows that fall between input start and end clinical trial start date
def filter_by_date(df, column, start='', end=''):
    if(start!='' and end!=''):
        try:
            # convert object to datetime type
            start = datetime.strptime(start, "%d/%m/%Y")
            end = datetime.strptime(end, "%d/%m/%Y")
            
            # get all dates in a range
            all_dates = []
            step = timedelta(days=1)
            while start <= end:
                all_dates.append(start.date().strftime("%d/%m/%Y"))
                start += step

            # filter dates in dataframes
            df = df[df[column].isin(all_dates)]
            
        except Exception as e:
            print(e)
            pass
    
    df = df.reset_index(drop=True)

    return df

# 2020-11-19
# 2021-07-29

# 14-12-2022
# 20 -12-2022