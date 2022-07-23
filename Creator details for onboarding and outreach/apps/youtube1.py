################################################# IMPORT DEPENDENCIES ##################################################
import sys
sys.path.append("../")
from packages import *
from proxy_authentication import *

def random_time_delay():
    time.sleep(random.uniform(25,35))

def get_channel_stats(youtube, channel_ids):
    all_data = []
    
    request = youtube.channels().list(
                part='snippet,contentDetails,statistics',
                id=','.join(channel_ids))
    
    response = request.execute()
    
    for i in range(len(response['items'])):
        data = {'customUrl':'', 'title':'', 'uploads':'', 'country':'', 'description':'', 'subscriberCount':'', 'viewCount':'', 'videoCount':''}
        for j in data.keys():
            if(j in ['customUrl','title','country','description']):
                try:
                    data[j] = response['items'][i]['snippet'][j]
                except:
                    data[j] = np.nan
                    pass
                
            elif(j in ['subscriberCount','viewCount','videoCount']):
                try:
                    data[j] = response['items'][i]['statistics'][j]
                except:
                    data[j] = np.nan
                    pass
            else:
                try:
                    data[j] = response['items'][i]['contentDetails']['relatedPlaylists'][j]
                except:
                    data[j] = np.nan
                    pass
            
              
        all_data.append(data)
    
    return all_data

def app():
    
    ################################################# SIDEBAR ##################################################
    st.sidebar.title('User Input Parameters')

    api_key = st.sidebar.text_input('GCP API Key', key='seven')
    email = st.sidebar.text_input('YouTube Email', key='two')
    passw = st.sidebar.text_input('YouTube Password', type='password', key='three')
    file = st.sidebar.file_uploader('Channel URLs', key = 'four')

    proxy_check = st.sidebar.checkbox('Use Proxy IP Address', key='zero')
    if(proxy_check==True):
        proxy_ip_port = st.sidebar.text_input('Proxy IP Address (IP:Port:Username:Password)', key='one')
    else:
        proxy_ip_port = ''

    button = st.sidebar.button('Submit',key='five')

    error_flag = False
    error_type = ''
    channel_urls = ''

    ################################################# BACKEND PROCESSING ##################################################

    # ---------------- CHECK INPUTS ----------------
    if(api_key=='' or email=='' or passw=='' or file is None or button==False):
        error_flag = True
        error_type = 'Empty Input Parameter'


    # ---------------- AUTHENTICATE PROXY ----------------
    if(proxy_check==True and error_flag==False):
        try:
            s=proxy_ip_port.split(':')
            ip=s[0]
            port=s[1]
            user=s[2]
            pas=s[3].strip()
            create_chromedriver(ip,port,user,pas)
        except Exception as e:
            #print(e)
            error_type = 'Proxy Authentication Error'
            error_flag = True

    
    # ---------------- CREATE AND OPEN DRIVER ----------------
    if(error_flag==False):
        try:
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
            #chrome_options.add_argument('--incognito')
            chrome_options.add_argument(f"user-agent={ua['google chrome']}")


            if(proxy_check==True):
                proxy = Proxy()
                proxy.proxy_type = ProxyType.MANUAL
                proxy.http_proxy = proxy_ip_port
                proxy.ssl_proxy = proxy_ip_port

                capabilities = webdriver.DesiredCapabilities.CHROME
                proxy.add_to_capabilities(capabilities)

                driver = uc.Chrome(executable_path=ChromeDriverManager().install(), 
                                   options=chrome_options,
                                   desired_capabilities=capabilities)
            else:
                driver = uc.Chrome(executable_path=ChromeDriverManager().install(), 
                                   options=chrome_options)

            driver.delete_all_cookies()
            random_time_delay()
            
        except Exception as e:
            error_type = e#'Driver Creation Error'
            error_flag = True

    # ---------------- Get Channel ID ----------------
    if(error_flag==False):
        channel_urls = list(pd.read_csv(file,header=None)[0].dropna(axis=0))
        channel_ids = []

        for url in channel_urls:
            try:
                driver.get(url)
                source = driver.page_source
                k = source[source.find('externalId'):source.find('keyword')].split('"')[2]
                channel_ids.append(k)
                random_time_delay()
            except:
                pass

        if(len(channel_urls)==0):
            error_type = 'Channel ID Extraction Error'
            error_flag = True

    # ---------------- Get Channel Statistics ----------------
    if(error_flag==False):
        try:
            youtube = build('youtube', 'v3', developerKey=api_key)
            channel_statistics = get_channel_stats(youtube, channel_ids)
            df1 = pd.DataFrame(channel_statistics)
            df1.columns = ['Channel_url','Channel_name','Playlist_id','Country','Description','Subscribers','Views','Total_videos']

            df1['Channel_url'] = df1['Channel_url'].apply(lambda x: 'https://www.youtube.com/c/'+x)
            df1['Channel_url'] = df1['Channel_url'].str.lower()
            df1['Subscribers'] = pd.to_numeric(df1['Subscribers'])
            df1['Views'] = pd.to_numeric(df1['Views'])
            df1['Total_videos'] = pd.to_numeric(df1['Total_videos'])
            print(df1)

        except Exception as e:
            error_type = e
            error_flag = True

    # ---------------- LOGIN ----------------
    if(error_flag==False):
        try:   
            # go to login page
            driver.get("https://accounts.google.com/signin/v2/identifier?service=youtube&uilel=3&passive=true&continue=https%3A%2F%2Fwww.youtube.com%2Fsignin%3Faction_handle_signin%3Dtrue%26app%3Ddesktop%26hl%3Den%26next%3Dhttps%253A%252F%252Fwww.youtube.com%252F&hl=en&ec=65620&flowName=GlifWebSignIn&flowEntry=ServiceLogin") 
            random_time_delay() 

            # Type the email address 
            emailid = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "identifier"))) 
            emailid.send_keys(email)
            random_time_delay()

            # Click on the next button
            nextButton = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "identifierNext")))
            ActionChains(driver).move_to_element(nextButton).click().perform()
            random_time_delay()

            # Type the password
            try:
                passwordid = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "password")))
                passwordid.send_keys(passw)

            except:
                passwordid = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.NAME, "password")))
                passwordid.send_keys(passw)
            random_time_delay()

            # Click on the signin button
            signinButton = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "passwordNext")))
            ActionChains(driver).move_to_element(signinButton).click().perform()
            random_time_delay()

        except Exception as e:
            #print(e)
            error_type = 'Login Error'
            error_flag = True


    # ---------------- Get Channel Email ----------------
    if(error_flag==False):

        final_urls = []
        email_ids = []
        locations = []
        external_urls = []

        for i,url in enumerate(channel_urls):
            print('Processing',i,'/',len(channel_urls))
            
            try:
                # go to channel
                driver.get(f"{url}/about".replace('//','/'))
                random_time_delay()

                # Click on View email address button
                driver.find_element_by_link_text('View email address'.upper()).click()
                random_time_delay()

                # Tick the checkbox 
                driver.find_elements_by_class_name('g-recaptcha')[0].click()
                random_time_delay()

                # Click on Submit button
                driver.find_element_by_id("submit-btn").click()
                random_time_delay()

                # parse HTML source page
                source = driver.page_source
                soup = bs(source, 'html.parser')

                final_urls.append(url)

                # Get email id
                try:
                    email = soup.find('a',{'id':'email'}).text
                except:
                    email = np.nan

                email_ids.append(email)
                print(email)
                
                # Get Location
                try:
                    loc = soup.find('div',{'id':'details-container'}).text.split(':')[-1].strip().lower()
                except:
                    loc = np.nan

                locations.append(loc)
                
                # Get external urls
                try:
                    lins_container = soup.find('div',{'id':'link-list-container'})
                    d = {}
                    for i in lins_container.find_all('a'):
                        d[i.text.strip().lower()] = i['href']
                except:
                    d = np.nan

                external_urls.append(d)
                
                random_time_delay()

            except Exception as e:
                print(e)
                #print('Some Error')
                pass
            
            print('*'*100)

        df3 = pd.DataFrame(zip(final_urls, email_ids, locations, external_urls),columns=['Channel_url','Email','Location','External URLs'])
        df3['Channel_url'] = df3['Channel_url'].str.lower()
        print(df3)

        if(len(df3.iloc[:,1:].dropna(how='all'))==0):
            error_type = 'Empty Df!! Channel Email Extraction Error'
            error_flag = True


    # ---------------- Get Final DataFrame ----------------
    if(error_flag==False):
        try:
            df4 = pd.merge(df1,
                        df3,
                        how="outer",
                        on='Channel_url')
        except:
            error_type = 'Df Merge Error'
            error_flag = True

    ################################################# MAIN PAGE ##################################################
    st.header('Input')

    if(button==True):
        st.write(channel_urls)

    for i in range(10):
        st.write('')

    st.header('Output')

    if(button==True and error_flag==True):
        st.error(error_type)

    if(button==True and error_flag==False):
        driver.quit()
        st.success('Extraction Complete!!')
        st.write(df4)
        st.download_button(label ='Download',
                            data = df4.to_csv(index=False).encode('utf-8'), 
                            file_name = 'Youtube1.csv',
                            mime = "text/csv",
                            key='six')