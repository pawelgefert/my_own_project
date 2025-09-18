import streamlit as st
import pandas as pd
import utils

#col1, col2 = st.columns(2)
#st.set_page_config(layout="wide")

#with col1:

#calc = st.container(horizontal=True, horizontal_alignment="left")


#with calc:
st.title("Kalkulator Kredytowy")

st.write("### Wprowadź szczegóły kredytu")
col1, col2, col3, col4 = st.columns(4, gap="small", vertical_alignment="center")
loan_amount = col1.number_input("Kwota kredytu", min_value=0, value=300000, step=1000)
interest_rate = col2.number_input("Oprocentowanie (%)", min_value=0.0, value=7.0, step=0.01)
number_of_payments = col3.number_input("Okres spłaty (miesiące)", min_value=1, value=60)
payments_type =col4.selectbox("Rodzaj rat", ["Równe", "Malejące"])

simulate_extra = st.checkbox("Symuluj dodatkowe spłaty")

extra_payments = {}
if simulate_extra:
    months = list(range(1, number_of_payments + 1))
    selected_months = st.multiselect("Wybierz miesiące dodatkowych spłat", months)
    for month in selected_months:
        amount = st.number_input(
            f"Dodatkowa spłata w miesiącu {month}",
            min_value=0.0, value=0.0, step=100.0, key=f"extra_{month}"
        )
        if amount > 0:
            extra_payments[month] = amount

# Pass extra_payments to your function
df = utils.calculate_loan_payment_schedule(
    loan_amount, interest_rate, number_of_payments, payments_type, extra_payments
)

#df = utils.calculate_loan_payment_schedule(loan_amount, interest_rate, number_of_payments, payments_type)

# Display the repayments.
total_payment = df['Rata'].sum()
total_interest = df['Odsetki'].sum()

st.write("### Wyniki")
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
col1.metric(label="Rata", value=f"{df['Rata'][0]:,.2f}")
col2.metric(label="Suma odsetek", value=f"{total_interest:,.0f}")


payments_df = df[["Rok", "Pozostałe Saldo"]].groupby("Rok").min()

# Display the data-frame as a chart.

st.write("### Harmonogram spłat")
st.dataframe(df.set_index('Miesiąc').style.format({
    'Miesiąc': '{:.0f}',
    'Rata': '{:,.2f}',
    'Kapitał': '{:,.2f}',
    'Odsetki': '{:,.2f}',
    'Pozostałe Saldo': '{:,.2f}'
}))

#col1, col2 = st.columns(2)
#with col1:
st.write("### Wykres spłat")
st.bar_chart(df.set_index('Miesiąc')[['Kapitał', 'Odsetki']])

#col1, col2 = st.columns(2)
#with col2:
st.write("### Wykres pozostałego salda")
st.line_chart(payments_df)








