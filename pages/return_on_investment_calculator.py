import streamlit as st
import pandas as pd

#st.set_page_config(layout="wide")

st.title("Kalkulator Zwrotu z Inwestycji")
col1, col2, col3, col4 = st.columns(4, gap="small", vertical_alignment="center")
initial_balance = col1.number_input("Kapitał początkowy", min_value=0, value=50000, step=1000)
yearly_contribution = col2.number_input("Roczna składka", min_value=0, value=50000, step=1000)
annual_rate_of_return = col3.number_input("Oprocentowanie (%)", min_value=0.0, value=5.0, step=0.01)
years = col4.number_input("Liczba lat", min_value=1, value=30)

def calculate_future_value_table(initial_balance, yearly_contribution, annual_rate_of_return, years):
    schedule = []
    for year in range(1, years + 1):
        if year == 1:
            end_balance = initial_balance * (1 + annual_rate_of_return / 100)
        else:
            end_balance = ((end_balance + yearly_contribution) * (1 + annual_rate_of_return / 100))
        
        schedule.append(
            [
                year,
                end_balance
            ]
        )
    df = pd.DataFrame(schedule, columns=["Rok", "Kapitał"])

    return df

df = calculate_future_value_table(initial_balance, yearly_contribution, annual_rate_of_return, years)

col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

with col1:
    st.dataframe(df.set_index('Rok').style.format({
        'Rok': '{:.0f}',    
        'Kapitał': '{:,.2f}'
    }))


