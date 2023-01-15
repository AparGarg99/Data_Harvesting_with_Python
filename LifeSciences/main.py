from packages import *
from multiapp import MultiApp
from apps import home, a_google_finance, b_google_patent, c_clinical_trial
from apps import d_google_news, e_biospace_news, f_fierce_pharma, g_fierce_biotech, h_populate_template

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
app.add_app("Google Finance", a_google_finance.app)
app.add_app("Google Patents", b_google_patent.app)
app.add_app("Clinical Trials", c_clinical_trial.app)
app.add_app("Populate Template", h_populate_template.app)
app.add_app("Google News", d_google_news.app)
app.add_app("BioSpace News", e_biospace_news.app)
app.add_app("FiercePharma News", f_fierce_pharma.app)
app.add_app("FierceBiotech News", g_fierce_biotech.app)


# The main app
app.run()