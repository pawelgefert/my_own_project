import streamlit as st
import pandas as pd
import utils

st.set_page_config(layout="centered")

st.title("Kalkulator Zwrotu z Inwestycji")
col1, col2, col3, col4 = st.columns(4, gap="small", vertical_alignment="center")
initial_balance = col1.number_input("Kapitał początkowy", min_value=0, value=50000, step=1000)
yearly_contribution = col2.number_input("Roczna składka", min_value=0, value=50000, step=1000)
annual_rate_of_return = col3.number_input("Oprocentowanie (%)", min_value=0.0, value=5.0, step=0.01)
years = col4.number_input("Liczba lat", min_value=1, value=30)



df = utils.calculate_future_value_schedule(initial_balance, yearly_contribution, annual_rate_of_return, years)

col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

with col1:
    st.dataframe(df.set_index('Rok').style.format({
        'Rok': '{:.0f}',    
        'Kapitał': '{:,.2f}'
    }))


