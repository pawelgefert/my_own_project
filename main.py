import streamlit as st
import config
from PIL import Image


# --- PAGE SETUP ---

#logo = Image.open("/Users/pawel/Python/my_own_project/images/logo.png")
logo = Image.open(config.IMAGES_DIR+ f"/logo.png")

st.logo(logo)
st.sidebar.text("")

about_page = st.Page(page="pages/about_me.py", 
                     title="O Mnie", 
                     icon=":material/account_circle:",
                     default=True)
loan_calculator_page = st.Page(page="pages/loan_calculator.py", 
                          title="Kalkulator Kredytowy", 
                          icon=":material/calculate:")

return_on_investment_claculator_page = st.Page(page="pages/return_on_investment_calculator.py", 
                          title="Kalkulator Zwrotu z Inwestycji", 
                          icon=":material/calculate:")

# --- PAGE NAVIGATION ---
pg = st.navigation({
    "": [about_page],
    "Kalkulatory": [loan_calculator_page, return_on_investment_claculator_page]
    })


pg.run()


