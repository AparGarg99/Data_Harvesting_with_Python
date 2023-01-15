import sys
sys.path.append("../")
from packages import *
from backend import fierce_biotech

def app():
    ################################################# SIDEBAR ##################################################
    st.sidebar.title('Input Parameters')

    query_flag = st.sidebar.checkbox('Query', value=False)
    if(query_flag==False):
        query = ''
    else:
        query = st.sidebar.text_input('Query', value='raises financing')


    date_filter_flag = st.sidebar.checkbox('Date Filter', key='twentysix')
    if(date_filter_flag==True):
        start = st.sidebar.date_input(label='Start Date', value=None, key='twentyseven') #'' #'01/01/2020'
        start = str(start.strftime(r"%d/%m/%Y"))

        end = st.sidebar.date_input(label='End Date', value=None, key='twentyeight') # '' #'31/12/2020'
        end = str(end.strftime(r"%d/%m/%Y"))
    else:
        start = ''
        end = ''

    button = st.sidebar.button('Submit', key='twentynine')

    ################################################# MAIN PAGE ################################################
    st.header('Output')

    if(button==True):
        fierce_biotech().scrape(query, start, end)

        st.success('Extraction Complete!!')