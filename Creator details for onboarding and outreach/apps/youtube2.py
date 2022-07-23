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

    api_key = st.sidebar.text_input('GCP API Key', key='twentytwo')
    file = st.sidebar.file_uploader('Channel URLs', key = 'twentythree')

    proxy_check = st.sidebar.checkbox('Use Proxy IP Address', key='twentyfour')
    if(proxy_check==True):
        proxy_ip_port = st.sidebar.text_input('Proxy IP Address (IP:Port:Username:Password)', key='twentyfive')
    else:
        proxy_ip_port = ''

    button = st.sidebar.button('Submit',key='twentysix')

    error_flag = False
    error_type = ''
    channel_urls = ''

    ################################################# BACKEND PROCESSING ##################################################

    # ---------------- CHECK INPUTS ----------------
    if(api_key=='' or file is None or button==False):
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

    # ---------------- Get Recommended Channels ----------------
    if(error_flag==False):

        final_playlist_ids = []
        rec_channels = []

        for t,playlist_id in enumerate(df1['Playlist_id']):
            print('Processing',t,'/',len(df1['Playlist_id']))

            try:
                l1 = []
                d = {}
                driver.get(f'https://www.youtube.com/playlist?list={playlist_id}')
                time.sleep(30)

                # parse HTML source page
                source = driver.page_source
                soup = bs(source, 'html.parser')
                time.sleep(30)

                final_playlist_ids.append(playlist_id)

                # Get recommended channels
                try: 
                    l1 = [f'https://www.youtube.com{i["href"]}'.split('&')[0] for i in soup.find_all('a',{'id':'video-title'})[:5]]
                    print(l1)
                    time.sleep(30)

                    for video in l1:
                        # Go to video
                        driver.get(video)
                        time.sleep(2*60)

                        # parse HTML source page
                        source = driver.page_source
                        soup = bs(source, 'html.parser')

                        # Get recommended channels
                        k = soup.find_all('yt-formatted-string',{'class':'style-scope ytd-channel-name'})
                        d[video] = set([i.text.strip() for i in k])
                        print(d)
                        random_time_delay()
                        
                except:
                    d = np.nan

                rec_channels.append(d)

                random_time_delay()

            except Exception as e:
                print(e)
                #print('Some Error')
                pass

            print('*'*100)

        df2 = pd.DataFrame(zip(final_playlist_ids, rec_channels),columns=['Playlist_id','Recommended_channels'])
        print(df2)

        if(len(df2.iloc[:,1:].dropna(how='all'))==0):
            error_type = 'Empty Df!! Recommended Channels Extraction Error'
            error_flag = True

    # ---------------- Get Final DataFrame ----------------
    if(error_flag==False):
        try:
            df3 = pd.merge(df1,
                        df2,
                        how="outer",
                        on='Playlist_id')

            df3 = df3[['Channel_url','Channel_name','Recommended_channels']]

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
        st.write(df3)
        st.download_button(label ='Download',
                            data = df3.to_csv(index=False).encode('utf-8'), 
                            file_name = 'Youtube2.csv', 
                            mime = "text/csv",
                            key='twentyseven')