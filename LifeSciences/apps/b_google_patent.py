import sys
sys.path.append("../")
from packages import *
from backend import google_patent

def app():
    ################################################# SIDEBAR ##################################################
    st.sidebar.title('Input Parameters')

    file = st.sidebar.file_uploader('Companies', key = 'three') # Get list of non-public companies

    date_filter_flag = st.sidebar.checkbox('Date Filter', key='four')

    if(date_filter_flag==True):
        start = st.sidebar.date_input(label='Start Date', value=None, key='five') #'' #'01/01/2020'
        start = str(start.strftime(r"%d/%m/%Y"))

        end = st.sidebar.date_input(label='End Date', value=None, key='six') # '' #'31/12/2020'
        end = str(end.strftime(r"%d/%m/%Y"))
    else:
        start = ''
        end = ''

    button = st.sidebar.button('Submit', key='seven')

    ################################################# MAIN PAGE ################################################
    st.header('Output')

    if(button==True):
        company_list = list(pd.read_csv(file,header=None)[0].dropna(axis=0)) 

        google_patent().scrape(company_list, start, end)

        st.success('Extraction Complete!!')