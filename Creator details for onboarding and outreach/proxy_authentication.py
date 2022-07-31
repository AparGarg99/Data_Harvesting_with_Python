from packages import *

def create_chromedriver(PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS):
    
    manifest_json = """
    {
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
    }
    """

    background_js = """
    var config = {
        mode: "fixed_servers",
        rules: {
        singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
        },
        bypassList: ["localhost"]
        }
    };

    chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

    function callbackFn(details) {
        return {
            authCredentials: {
            username: "%s",
            password: "%s"
            }
        };
    }

    chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
    );
    """ % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)


    def get_chromedriver(use_proxy=True):
        chrome_options = uc.ChromeOptions()
      
        pluginfile = 'proxy_auth_plugin.zip'
        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)   
        chrome_options.add_extension(pluginfile)
        
        chrome_options.add_experimental_option("detach", True)
        chrome_options.add_argument("--mute-audio")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36")
        
        driver =  uc.Chrome(executable_path=ChromeDriverManager().install(),
                            chrome_options=chrome_options)
        return driver

    driver = get_chromedriver(use_proxy=True)
    driver.get("https://whatismyipaddress.com/")
    time.sleep(60)
    driver.quit()

