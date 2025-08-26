import streamlit as st
import pandas as pd
#import matplotlib.pyplot as plt
import math

#st.set_page_config(layout="wide")

st.title("Kalkulator Kredytowy")

st.write("### Wprowadź szczegóły kredytu")
col1, col2, col3, col4 = st.columns(4, gap="small", vertical_alignment="center")
loan_amount = col1.number_input("Kwota kredytu", min_value=0, value=300000, step=1000)
interest_rate = col2.number_input("Oprocentowanie (%)", min_value=0.0, value=7.0, step=0.01)
number_of_payments = col3.number_input("Okres spłaty (miesiące)", min_value=1, value=60)
payments_type =col4.selectbox("Rodzaj rat", ["Równe", "Malejące"])

# Calculate the repayments.
monthly_interest_rate = (interest_rate / 100) / 12
#number_of_payments = loan_term * 12

if payments_type == "Równe":
    # For annuity payments, we use the formula for fixed monthly payments.

    monthly_payment = (
        loan_amount
        * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
        / ((1 + monthly_interest_rate) ** number_of_payments - 1)
    )

    # Create a data-frame with the payment schedule.
    schedule = []
    remaining_balance = loan_amount
    for i in range(1, number_of_payments + 1):
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = monthly_payment - interest_payment
        remaining_balance -= principal_payment
        year = math.ceil(i / 12) 
        schedule.append(
            [
                i,
                year,
                monthly_payment,
                principal_payment,
                interest_payment,
                remaining_balance
            ]
        )


elif payments_type == "Malejące":
    #monthly_payment = (loan_amount * monthly_interest_rate) + (loan_amount / number_of_payments)   

    # Create a data-frame with the payment schedule.
    schedule = []
    remaining_balance = loan_amount
    for i in range(1, number_of_payments + 1):
        monthly_payment = (remaining_balance * monthly_interest_rate) + (loan_amount / number_of_payments)
        interest_payment = remaining_balance * monthly_interest_rate
        principal_payment = loan_amount/ number_of_payments
        remaining_balance -= principal_payment
        year = math.ceil(i / 12) 
        schedule.append(
            [
                i,
                year,
                monthly_payment,
                principal_payment,
                interest_payment,
                remaining_balance
            ]
        ) 
    

df = pd.DataFrame(schedule, columns=["Miesiąc", "Rok", "Rata", "Kapitał", "Odsetki", "Pozostałe Saldo"])

# Display the repayments.
#total_payments = monthly_payment * number_of_payments
#total_interest = total_payments - loan_amount
total_payment = df['Rata'].sum()
total_interest = df['Odsetki'].sum()

st.write("### Wyniki")
col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
#col1.metric(label="Rata", value=f"{monthly_payment:,.2f}")
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
#}).hide(axis='index'))
}))

col1, col2 = st.columns(2)
with col1:
    st.write("### Wykres spłat")
    st.bar_chart(df.set_index('Miesiąc')[['Kapitał', 'Odsetki']])

#col1, col2 = st.columns(2)
with col2:
    st.write("### Wykres pozostałego salda")
    st.line_chart(payments_df)


def calculate_payment_schedule(loan_amount, monthly_interest_rate, number_of_payments, type="annuity"):
    schedule = []
    remaining_balance = loan_amount
    if type == "annuity":
        monthly_payment = (
            loan_amount
            * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
            / ((1 + monthly_interest_rate) ** number_of_payments - 1)
        )

        for i in range(1, number_of_payments + 1):
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment
            year = math.ceil(i / 12) 
            schedule.append(
                [
                    i,
                    year,
                    monthly_payment,
                    principal_payment,
                    interest_payment,
                    remaining_balance
                ]
            )
    elif type == "decreasing":
        for i in range(1, number_of_payments + 1):
            monthly_payment = (remaining_balance * monthly_interest_rate) + (loan_amount / number_of_payments)
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = loan_amount / number_of_payments
            remaining_balance -= principal_payment
            year = math.ceil(i / 12) 
            schedule.append(
                [
                    i,
                    year,
                    monthly_payment,
                    principal_payment,
                    interest_payment,
                    remaining_balance
                ]
            )
    return pd.DataFrame(schedule, columns=["Miesiąc", "Rok", "Rata", "Kapitał", "Odsetki", "Pozostałe Saldo"])
