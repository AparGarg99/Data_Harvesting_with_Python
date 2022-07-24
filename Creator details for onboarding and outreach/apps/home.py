import streamlit as st
from PIL import Image

def app():
    text = "Harvesting creator details for onboarding and outreach"
    st.markdown(f"<h1 style='text-align: center; color:#e3edd1; font-size:480%; font-family:Brush Script MT, cursive;'>{text}</h1>", unsafe_allow_html=True)

    for i in range(5):
        st.write('')

    img = Image.open('logo.png')

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write(' ')

    with col2:
        st.image(img,width=350)

    with col3:
        st.write(' ')

    with col4:
        st.write(' ')
    
    