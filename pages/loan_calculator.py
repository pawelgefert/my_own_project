import streamlit as st
import pandas as pd
import utils

st.title("Kalkulator Kredytowy")

st.write("### Wprowadź szczegóły kredytu")
col1, col2, col3, col4 = st.columns(4, gap="small", vertical_alignment="center")
loan_amount = col1.number_input("Kwota kredytu", min_value=0, value=300000, step=1000)
interest_rate = col2.number_input("Oprocentowanie (%)", min_value=0.0, value=7.0, step=0.01)
number_of_payments = col3.number_input("Okres spłaty (miesiące)", min_value=1, value=60)
payments_type = col4.selectbox("Rodzaj rat", ["Równe", "Malejące"])

# Initialize session state for extra payments
if "extra_payments" not in st.session_state:
    st.session_state.extra_payments = {}

simulate_extra = st.checkbox("Symuluj dodatkowe spłaty")

extra_payments = {}

if simulate_extra:
    months = list(range(1, number_of_payments + 1))
    selected_months = st.multiselect(
        "Wybierz miesiące dodatkowych spłat", 
        months, 
        default=list(st.session_state.extra_payments.keys())
    )
    for month in selected_months:
        amount = st.number_input(
            f"Dodatkowa spłata w miesiącu {month}",
            min_value=0.0, value=st.session_state.extra_payments.get(month, 0.0), step=100.0, key=f"extra_{month}"
        )
        if amount > 0:
            extra_payments[month] = amount

    # Update session state
    st.session_state.extra_payments = extra_payments


st.write("## Porównanie scenariuszy" if simulate_extra else "### Wyniki")


if simulate_extra:
    st.set_page_config(layout="wide")
    colA, colB = st.columns(2)

    with colA:
        st.subheader("Scenariusz 1: Skrócenie okresu spłaty")
        df_shorter = utils.calculate_loan_payment_schedule(
            loan_amount, interest_rate, number_of_payments, payments_type, extra_payments, scenario="shorter_term"
        )
        total_payment_shorter = df_shorter['Rata'].sum()
        total_interest_shorter = df_shorter['Odsetki'].sum()
        # Display metrics side by side
        met_col1, met_col2, met_col3 = st.columns(3)
        met_col1.metric(label="Rata", value=f"{df_shorter['Rata'][0]:,.2f}")
        met_col2.metric(label="Suma odsetek", value=f"{total_interest_shorter:,.0f}")
        met_col3.metric(label="Liczba rat", value=f"{len(df_shorter)}")

        st.write("### Harmonogram spłat")
        st.dataframe(df_shorter.set_index('Miesiąc').style.format({
            'Miesiąc': '{:.0f}',
            'Rata': '{:,.2f}',
            'Kapitał': '{:,.2f}',
            'Odsetki': '{:,.2f}',
            'Pozostałe Saldo': '{:,.2f}'
        }))
        st.write("### Wykres spłat")
        st.bar_chart(df_shorter.set_index('Miesiąc')[['Kapitał', 'Odsetki']])
        payments_df_shorter = df_shorter[["Rok", "Pozostałe Saldo"]].groupby("Rok").min()
        

    with colB:
        st.subheader("Scenariusz 2: Stała liczba rat, niższa rata")
        df_fixed = utils.calculate_loan_payment_schedule(
            loan_amount, interest_rate, number_of_payments, payments_type, extra_payments, scenario="fixed_term"
        )
        total_payment_fixed = df_fixed['Rata'].sum()
        total_interest_fixed = df_fixed['Odsetki'].sum()
        # Display metrics side by side
        met_col1, met_col2, met_col3 = st.columns(3)
        met_col1.metric(label="Rata (pierwsza)", value=f"{df_fixed['Rata'][0]:,.2f}")
        met_col2.metric(label="Suma odsetek", value=f"{total_interest_fixed:,.0f}")
        met_col3.metric(label="Liczba rat", value=f"{len(df_fixed)}")

        st.write("### Harmonogram spłat")
        st.dataframe(df_fixed.set_index('Miesiąc').style.format({
            'Miesiąc': '{:.0f}',
            'Rata': '{:,.2f}',
            'Kapitał': '{:,.2f}',
            'Odsetki': '{:,.2f}',
            'Pozostałe Saldo': '{:,.2f}'
        }))
        st.write("### Wykres spłat")
        st.bar_chart(df_fixed.set_index('Miesiąc')[['Kapitał', 'Odsetki']])
        payments_df_fixed = df_fixed[["Rok", "Pozostałe Saldo"]].groupby("Rok").min()

else:
    #st.subheader("Scenariusz 1: Skrócenie okresu spłaty")
    extra_payments = st.session_state.extra_payments
    st.set_page_config(layout="centered")
    df_shorter = utils.calculate_loan_payment_schedule(
        loan_amount, interest_rate, number_of_payments, payments_type, {}, scenario="shorter_term"
    )
    total_payment_shorter = df_shorter['Rata'].sum()
    total_interest_shorter = df_shorter['Odsetki'].sum()
    # Display metrics side by side
    met_col1, met_col2 = st.columns(2)
    met_col1.metric(label="Rata", value=f"{df_shorter['Rata'][0]:,.2f}")
    met_col2.metric(label="Suma odsetek", value=f"{total_interest_shorter:,.0f}")
    #st.metric(label="Liczba rat", value=f"{len(df_shorter)}")
    st.write("### Harmonogram spłat")
    st.dataframe(df_shorter.set_index('Miesiąc').style.format({
        'Miesiąc': '{:.0f}',
        'Rata': '{:,.2f}',
        'Kapitał': '{:,.2f}',
        'Odsetki': '{:,.2f}',
        'Pozostałe Saldo': '{:,.2f}'
    }))
    st.write("### Wykres spłat")
    st.bar_chart(df_shorter.set_index('Miesiąc')[['Kapitał', 'Odsetki']])
    payments_df_shorter = df_shorter[["Rok", "Pozostałe Saldo"]].groupby("Rok").min()
