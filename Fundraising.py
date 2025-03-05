import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

class FundRaising:
    def __init__(self, company_name, project_cost):
        self.company_name = company_name
        self.project_cost = project_cost
        self.funds_raised = 0
        self.fund_sources = {'IPO': 0, 'Private Equity': 0, 'Debt': 0, 'Preference Shares': 0}

    def ipo(self, ipo_price_per_share, shares_to_issue):
        raised = ipo_price_per_share * shares_to_issue
        self.funds_raised += raised
        self.fund_sources['IPO'] += raised
        return raised

    def private_equity(self, equity_percentage, investment_amount):
        raised = (equity_percentage / 100) * self.project_cost  # Now scaled to project cost
        raised = min(raised, investment_amount)  # Ensure it does not exceed investment amount
        self.funds_raised += raised
        self.fund_sources['Private Equity'] += raised
        return raised

    def debt(self, loan_amount):
        raised = min(loan_amount, self.project_cost - self.funds_raised)  # Limit to remaining funds
        self.funds_raised += raised
        self.fund_sources['Debt'] += raised
        return raised

    def preference_shares(self, number_of_shares, price_per_share):
        raised = number_of_shares * price_per_share
        self.funds_raised += raised
        self.fund_sources['Preference Shares'] += raised
        return raised

    def plot_fund_split(self):
        labels = []
        values = []
        
        for key, value in self.fund_sources.items():
            if value > 0:
                labels.append(key)
                values.append(value)
        
        if sum(values) == 0:
            st.warning("No funds raised yet! Please add funds to view the pie chart.")
            return
        
        plt.figure(figsize=(8, 8))
        plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=['#ff9999','#66b3ff','#99ff99','#ffcc99'])
        plt.title(f"Fundraising Split for {self.company_name}")
        plt.axis('equal')
        st.pyplot(plt)

    def display_table(self):
        data = {'Source': list(self.fund_sources.keys()), 'Funds Raised (INR)': list(self.fund_sources.values())}
        df = pd.DataFrame(data)
        st.write("### Funds Raised by Source")
        st.dataframe(df)

st.title("Mining Project Fundraising Calculator")
company_name = st.text_input("Enter Company Name:")
project_cost = st.number_input("Enter Total Project Cost (INR):", min_value=0.0, format="%.2f")

if "fund_raising" not in st.session_state:
    st.session_state.fund_raising = FundRaising(company_name, project_cost)
fund_raising = st.session_state.fund_raising

st.write("## Select a Method to Raise Funds")
method_choice = st.radio("Choose a funding method:", ("IPO", "Private Equity", "Debt", "Preference Shares"))

if method_choice == "IPO":
    ipo_price_per_share = st.number_input("Enter IPO Price Per Share (INR):", min_value=0.0, format="%.2f")
    shares_to_issue = st.number_input("Enter Number of Shares to Issue:", min_value=0, format="%d")
    if st.button("Raise Funds via IPO"):
        fund_raising.ipo(ipo_price_per_share, shares_to_issue)

elif method_choice == "Private Equity":
    equity_percentage = st.number_input("Enter Equity Percentage to Offer:", min_value=0.0, max_value=100.0, format="%.2f")
    investment_amount = st.number_input("Enter Investment Amount (INR):", min_value=0.0, format="%.2f")
    if st.button("Raise Funds via Private Equity"):
        fund_raising.private_equity(equity_percentage, investment_amount)

elif method_choice == "Debt":
    loan_amount = st.number_input("Enter Loan Amount (INR):", min_value=0.0, format="%.2f")
    if st.button("Raise Funds via Debt"):
        fund_raising.debt(loan_amount)

elif method_choice == "Preference Shares":
    number_of_shares = st.number_input("Enter Number of Preference Shares:", min_value=0, format="%d")
    price_per_share = st.number_input("Enter Price Per Preference Share (INR):", min_value=0.0, format="%.2f")
    if st.button("Raise Funds via Preference Shares"):
        fund_raising.preference_shares(number_of_shares, price_per_share)

st.write(f"### Total Funds Raised: {fund_raising.funds_raised:.2f} INR")
remaining_funds = project_cost - fund_raising.funds_raised
if remaining_funds > 0:
    st.write(f"Remaining funds required: {remaining_funds:.2f} INR")
else:
    st.write("Funds raised are sufficient to cover the project cost!")

fund_raising.plot_fund_split()
fund_raising.display_table()
