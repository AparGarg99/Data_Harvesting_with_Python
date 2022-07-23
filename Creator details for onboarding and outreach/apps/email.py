################################################# IMPORT DEPENDENCIES ##################################################
import sys
sys.path.append("../")
from packages import *

def verify_email(api_key,email_id):
  try:
    response = requests.get(f"https://api.hunter.io/v2/email-verifier?email={email_id}&api_key={api_key}")
    resp = response.json()['data']
    if(resp['result']!='undeliverable' and resp['regexp']==True and resp['gibberish']==False):
      check = 'Valid'
    else:
      check = 'Invalid'

  except Exception as e:
    check = 'API not working'

  return check


def app():  
    ################################################# SIDEBAR ##################################################
    st.sidebar.title('User Input Parameters')

    api_key = st.sidebar.text_input('API Key', key='twentyeight',value='f8f32972f406336ffff3ad68293ea7e65dbdc390')
    email_subject = st.sidebar.text_input('Email Subject', key='twentynine',value='rgrgrgr')
    sender_email_address = st.sidebar.text_input('Sender Email Address', key='thirty',value='aparworkstuff@gmail.com')
    sender_password = st.sidebar.text_input('Sender Email Password', type='password', key='thirtyone',value='wawxozaeuyvvoebj')
    receiver_email_address = st.sidebar.file_uploader('Receiver Email Address', key = 'thirtytwo')
    email_content = st.text_area('Body of Email', key ='thirtythree',value='fefefeffwe')
    attachments = st.sidebar.file_uploader('Email Attachments', key = 'thirtyfour')
    button = st.sidebar.button('Submit',key='thirtyfive')

    error_flag = False
    error_type = ''

    ################################################# BACKEND PROCESSING ##################################################

    # ---------------- CHECK INPUTS ----------------
    if(api_key=='' or email_subject=='' or sender_email_address=='' or sender_password=='' or receiver_email_address is None or button==False):
        error_flag = True
        error_type = 'Empty Input Parameter'

    # ---------------- VERIFY SENDER EMAIL ID ----------------
    if(error_flag==False):
        verify_sender_email_address = verify_email(api_key,sender_email_address)

        if(verify_sender_email_address=='Invalid'):
            error_flag = True
            error_type = "Couldn't Verify Sender Email Address"

    # ---------------- VERIFY RECEIVER EMAIL IDs ----------------
    if(error_flag==False):
        receiver_email_address = list(pd.read_csv(receiver_email_address,header=None)[0].dropna(axis=0))
        email_list = {}

        for i in receiver_email_address:
            email_list[i] = verify_email(api_key,i)

        email_list = [key for key, value in email_list.items() if value=='Valid']

        if(email_list==[]):
            error_flag = True
            error_type = "Couldn't Verify Any Receiver Email Address"

    # ---------------- SEND EMAIL ----------------
    if(error_flag==False):
      msg = EmailMessage()
      msg['Subject'] = email_subject
      msg['From'] = sender_email_address
      msg['To'] = ", ".join(email_list)

      msg.set_content(email_content)

      msg.add_attachment(attachments.read(),maintype="application",subtype="octet-stream",filename=attachments.name)

      with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
          smtp.login(sender_email_address, sender_password)
          smtp.send_message(msg)
        

    ################################################# MAIN PAGE ##################################################

    if(button==True and error_flag==True):
        st.error(error_type)

    if(button==True and error_flag==False):
        st.write(receiver_email_address)
        st.write(sender_email_address)
        st.success('Emails Sent!!')