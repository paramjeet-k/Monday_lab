import streamlit as st
import pandas as pd

class FundRaising:
    def __init__(self, company_name, project_cost):
        self.company_name = company_name
        self.project_cost = project_cost
        self.funds_raised = 0
        self.fund_sources = {'IPO': 0, 'Private Equity': 0, 'Debt': 0, 'Preference Shares': 0}

    def raise_funds(self, ipo_amount, pe_amount, debt_amount, ps_amount):
        remaining_needed = self.project_cost - self.funds_raised
        
        funding_options = [
            ('IPO', ipo_amount),
            ('Private Equity', pe_amount),
            ('Debt', debt_amount),
            ('Preference Shares', ps_amount)
        ]
        
        for source, amount in funding_options:
            if remaining_needed <= 0:
                break
            allocated_amount = min(amount, remaining_needed)
            self.funds_raised += allocated_amount
            self.fund_sources[source] += allocated_amount
            remaining_needed -= allocated_amount

    def display_table(self):
        data = {'Source': list(self.fund_sources.keys()), 'Funds Raised (INR)': list(self.fund_sources.values())}
        df = pd.DataFrame(data)
        st.write("### Funds Raised Breakdown")
        st.dataframe(df)

st.title("Mining Project Fundraising Calculator")
company_name = st.text_input("Enter Company Name:")
project_cost = st.number_input("Enter Total Project Cost (INR):", min_value=0.0, format="%.2f")

if "fund_raising" not in st.session_state or st.session_state.fund_raising.company_name != company_name:
    st.session_state.fund_raising = FundRaising(company_name, project_cost)
fund_raising = st.session_state.fund_raising

st.write("## Enter the Maximum Amount You Can Raise from Each Source")
ipo_amount = st.number_input("Maximum IPO Amount (INR):", min_value=0.0, format="%.2f")
pe_amount = st.number_input("Maximum Private Equity Amount (INR):", min_value=0.0, format="%.2f")
debt_amount = st.number_input("Maximum Debt Amount (INR):", min_value=0.0, format="%.2f")
ps_amount = st.number_input("Maximum Preference Shares Amount (INR):", min_value=0.0, format="%.2f")

if st.button("Calculate Fundraising Plan"):
    fund_raising.raise_funds(ipo_amount, pe_amount, debt_amount, ps_amount)
    
st.write(f"### Total Funds Raised: {fund_raising.funds_raised:.2f} INR")
remaining_funds = project_cost - fund_raising.funds_raised
if remaining_funds > 0:
    st.write(f"Remaining funds required: {remaining_funds:.2f} INR")
else:
    st.write("Funds raised are sufficient to cover the project cost!")

fund_raising.display_table()
