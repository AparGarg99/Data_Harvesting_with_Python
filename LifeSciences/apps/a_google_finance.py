import sys
sys.path.append("../")
from packages import *
from backend import google_finance

def app():
    ################################################# SIDEBAR ##################################################
    st.sidebar.title('Input Parameters')

    file = st.sidebar.file_uploader('Companies', key = 'one')

    button = st.sidebar.button('Submit', key='two')

    ################################################# MAIN PAGE ################################################
    st.header('Output')

    if(button==True):
        company_list = list(pd.read_csv(file,header=None)[0].dropna(axis=0))

        google_finance().scrape(company_list)

        st.success('Extraction Complete!!')