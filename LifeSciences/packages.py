########################### Import Dependencies ########################## 
import bs4
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
import undetected_chromedriver as uc
from fake_useragent import UserAgent
import time
import os
import pandas as pd
import numpy as np
import re
import random
from tqdm import tqdm
from pathlib import Path
import webbrowser
import glob
import shutil
import requests
from datetime import datetime, timedelta, date
import argparse
import streamlit as st
import urllib3
import warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
warnings.filterwarnings("ignore")