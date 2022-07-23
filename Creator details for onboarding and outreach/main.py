import streamlit as st
from multiapp import MultiApp
from apps import home, instagram1, youtube1, instagram2, youtube2, email

app = MultiApp()

# Minimalize the default features
hide_menu_style = """
        <style>
        footer {visibility: hidden;}
        </style>
        """
st.markdown(hide_menu_style, unsafe_allow_html=True)


# Add all your application here
app.add_app("Home", home.app)
app.add_app("Instagram Details", instagram1.app)
app.add_app("Instagram Following", instagram2.app)
app.add_app("YouTube Details", youtube1.app)
app.add_app("YouTube Recommended", youtube2.app)
app.add_app("Send Emails",email.app)

# The main app
app.run()
