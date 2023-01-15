import sys
sys.path.append("../")
from packages import *
from backend import biospace_news

def app():
    ################################################# SIDEBAR ##################################################
    st.sidebar.title('Input Parameters')

    query_flag = st.sidebar.checkbox('Query', value=False)
    if(query_flag==False):
        query = ''
    else:
        query = st.sidebar.text_input('Query', value='raises financing')


    date_filter_flag = st.sidebar.checkbox('Date Filter', key='eighteen')
    if(date_filter_flag==True):
        start = st.sidebar.date_input(label='Start Date', value=None, key='nineteen') #'' #'01/01/2020'
        start = str(start.strftime(r"%d/%m/%Y"))

        end = st.sidebar.date_input(label='End Date', value=None, key='twenty') # '' #'31/12/2020'
        end = str(end.strftime(r"%d/%m/%Y"))
    else:
        start = ''
        end = ''

    button = st.sidebar.button('Submit', key='twentyone')

    ################################################# MAIN PAGE ################################################
    st.header('Output')

    if(button==True):
        biospace_news().scrape(query, start, end)

        st.success('Extraction Complete!!')