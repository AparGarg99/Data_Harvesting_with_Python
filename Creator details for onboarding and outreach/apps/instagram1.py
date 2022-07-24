################################################# IMPORT DEPENDENCIES ##################################################
import sys
sys.path.append("../")
from packages import *
from proxy_authentication import *

def random_time_delay():
    time.sleep(random.uniform(40,80))

def app():
    
    ################################################# SIDEBAR ##################################################
    st.sidebar.title('User Input Parameters')

    username = st.sidebar.text_input('Instagram Username', key='nine')
    passw = st.sidebar.text_input('Instagram Password', type='password', key='ten')
    file = st.sidebar.file_uploader('Account URLs', key = 'eleven')

    proxy_check = st.sidebar.checkbox('Use Proxy IP Address', key='fourteen')
    if(proxy_check==True):
        proxy_ip_port = st.sidebar.text_input('Proxy IP Address (IP:Port:Username:Password)', key='eight')
    else:
        proxy_ip_port = ''

    button = st.sidebar.button('Submit',key='twelve')

    error_flag = False
    error_type = ''
    urls = ''

    ################################################# BACKEND PROCESSING ##################################################

    # ---------------- CHECK INPUTS ----------------
    if(username=='' or passw=='' or file is None or button==False):
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
        except:
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
        except:
            error_type = 'Driver Creation Error'
            error_flag = True

    # ---------------- LOGIN ----------------
    if(error_flag==False):
        try:
            # go to login page
            driver.get("https://www.instagram.com")
            random_time_delay()

            # Type username
            emailid = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "username"))) 
            emailid.send_keys(username)
            random_time_delay()

            # Type password
            passwordid = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.NAME, "password")))
            passwordid.send_keys(passw)
            random_time_delay()

            # Click on the signin button
            signinButton = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[3]/button/div')))
            ActionChains(driver).move_to_element(signinButton).click().perform()
            random_time_delay()
            
        except Exception as e:
            #print(e)
            error_type = 'Login Error'
            error_flag = True

    # ---------------- Get Account Statistics & Email ----------------
    if(error_flag==False):
        directory = '../instagram1_checkpoints'
        if not os.path.exists(directory):
            os.makedirs(directory)
        else:
            os.rmdir(directory)
            
        urls = list(pd.read_csv(file,header=None)[0].dropna(axis=0))
        df1 = []

        for i,url in enumerate(urls):
            print('Processing',i,'/',len(urls))
            
            try:
                # go to account
                driver.get(url)
                random_time_delay()
                x1 = url
                
                # Get Stats
                try:
                    x2 = [i.text for i in driver.find_elements_by_css_selector('span[class="_ac2a"]')]
                except:
                    x2 = np.nan
                
                # Get Description
                try:
                    x3 = driver.find_element_by_css_selector('div[class="_aa_c"]').text
                except:
                    x3 = np.nan
                    
                record = [x1,x2,x3]
                record = pd.DataFrame(record).T
                print(record.shape)
                print(record)
                
                df1.append(record)
                random_time_delay()
                
            except Exception as e:
                print('Some Error')

            pd.concat(df1).to_csv(f'../instagram1_checkpoints/checkpoint{i}.csv',index=False)
            
            print('*'*100)

        df1 = pd.concat(df1).reset_index(drop=True)
        df1.columns = ['Account_url','Stats','Description']
        df2 = df1.drop('Stats',axis=1)
        df3 = pd.DataFrame(df1["Stats"].to_list(), columns=['Total_posts', 'Following','Followers'])
        df4 = pd.concat([df2,df3],axis=1)
        df4['Email'] = df4['Description'].apply(lambda x: re.findall('\S+@\S+', str(x)))
        df4 = df4.replace([],np.nan).replace('[]',np.nan)
        print(df4)

        if(len(df4.iloc[:,1:].dropna(how='all'))==0):
            error_type = 'Empty Df!! Account Statistics Extraction Error'
            error_flag = True


    ################################################# MAIN PAGE ##################################################
    st.header('Input')

    if(button==True):
        st.write(urls)

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
                            file_name = 'Instagram1.csv',
                            mime = "text/csv",
                            key='thirteen')