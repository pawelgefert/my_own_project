import pandas as pd
import math

def calculate_loan_payment_schedule_orig(loan_amount, interest_rate, number_of_payments, payments_type):

    # Calculate the repayments.
    monthly_interest_rate = (interest_rate / 100) / 12
    #number_of_payments = loan_term * 12
    if payments_type == "Równe":

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

    return df

def calculate_loan_payment_schedule_v1(
    loan_amount, interest_rate, number_of_payments, payments_type, extra_payments=None
):
    if extra_payments is None:
        extra_payments = {}

    monthly_interest_rate = (interest_rate / 100) / 12

    schedule = []
    remaining_balance = loan_amount

    for i in range(1, number_of_payments + 1):
        year = math.ceil(i / 12)

        if payments_type == "Równe":
            monthly_payment = (
                loan_amount
                * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
                / ((1 + monthly_interest_rate) ** number_of_payments - 1)
            )
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = monthly_payment - interest_payment
        elif payments_type == "Malejące":
            monthly_payment = (remaining_balance * monthly_interest_rate) + (loan_amount / number_of_payments)
            interest_payment = remaining_balance * monthly_interest_rate
            principal_payment = loan_amount / number_of_payments

        # Apply extra payment if present
        extra_payment = extra_payments.get(i, 0)
        remaining_balance -= (principal_payment + extra_payment)

        schedule.append(
            [
                i,
                year,
                monthly_payment + extra_payment,
                principal_payment + extra_payment,
                interest_payment,
                remaining_balance
            ]
        )

        # Stop if loan is paid off
        if remaining_balance <= 0:
            break

    df = pd.DataFrame(schedule, columns=["Miesiąc", "Rok", "Rata", "Kapitał", "Odsetki", "Pozostałe Saldo"])
    return df


def calculate_loan_payment_schedule(
    loan_amount, interest_rate, number_of_payments, payments_type, extra_payments=None, scenario="shorter_term"
):
    """
    scenario: 
        "shorter_term" - extra payments shorten the loan term (default)
        "fixed_term"   - extra payments lower the installment, term stays the same
    """
    import pandas as pd
    import math

    if extra_payments is None:
        extra_payments = {}

    monthly_interest_rate = (interest_rate / 100) / 12
    schedule = []
    remaining_balance = loan_amount

    for i in range(1, number_of_payments + 1):
        year = math.ceil(i / 12)
        months_left = number_of_payments - i + 1

        # Scenario 1: Shorter term (installment fixed, term shortens)
        if scenario == "shorter_term":
            if payments_type == "Równe":
                monthly_payment = (
                    loan_amount
                    * (monthly_interest_rate * (1 + monthly_interest_rate) ** number_of_payments)
                    / ((1 + monthly_interest_rate) ** number_of_payments - 1)
                )
                interest_payment = remaining_balance * monthly_interest_rate
                principal_payment = monthly_payment - interest_payment
            elif payments_type == "Malejące":
                principal_payment = loan_amount / number_of_payments
                interest_payment = remaining_balance * monthly_interest_rate
                monthly_payment = principal_payment + interest_payment

            extra_payment = extra_payments.get(i, 0)
            total_principal = principal_payment + extra_payment

            # Adjust last payment if it would overpay
            if total_principal > remaining_balance:
                total_principal = remaining_balance
                monthly_payment = total_principal + interest_payment
                extra_payment = total_principal - principal_payment

            remaining_balance -= total_principal

            schedule.append(
                [
                    i,
                    year,
                    monthly_payment,
                    total_principal,
                    interest_payment,
                    max(remaining_balance, 0)
                ]
            )

            if remaining_balance <= 0:
                break

        # Scenario 2: Fixed term (installment recalculated, term fixed)
        elif scenario == "fixed_term":
            if payments_type == "Równe":
                monthly_payment = (
                    remaining_balance
                    * (monthly_interest_rate * (1 + monthly_interest_rate) ** months_left)
                    / ((1 + monthly_interest_rate) ** months_left - 1)
                )
                interest_payment = remaining_balance * monthly_interest_rate
                principal_payment = monthly_payment - interest_payment
            elif payments_type == "Malejące":
                principal_payment = loan_amount / number_of_payments
                interest_payment = remaining_balance * monthly_interest_rate
                monthly_payment = principal_payment + interest_payment

            extra_payment = extra_payments.get(i, 0)
            total_principal = principal_payment + extra_payment
            remaining_balance -= total_principal

            schedule.append(
                [
                    i,
                    year,
                    monthly_payment,
                    total_principal,
                    interest_payment,
                    max(remaining_balance, 0)
                ]
            )

    df = pd.DataFrame(schedule, columns=["Miesiąc", "Rok", "Rata", "Kapitał", "Odsetki", "Pozostałe Saldo"])
    return df







def calculate_future_value_schedule(initial_balance, yearly_contribution, annual_rate_of_return, years):
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