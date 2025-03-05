import streamlit as st
import pandas as pd
import numpy as np

class FundRaising:
    def __init__(self, company_name, project_cost):
        self.company_name = company_name
        self.project_cost = project_cost
        self.funds_raised = 0
        self.fund_sources = {'IPO': 0, 'Private Equity': 0, 'Debt': 0, 'Preference Shares': 0}
        self.financing_costs = {'Debt Interest': 0, 'Equity Dilution': 0, 'Debt EMI (Monthly)': 0, 'Total Debt Repayment': 0}

    def calculate_debt_emi(self, loan_amount, interest_rate, years):
        if loan_amount == 0:
            return 0, 0
        
        monthly_rate = (interest_rate / 100) / 12
        months = years * 12
        if monthly_rate > 0:
            emi = loan_amount * monthly_rate / (1 - (1 + monthly_rate) ** -months)
        else:
            emi = loan_amount / months
        total_payment = emi * months
        self.financing_costs['Debt Interest'] = total_payment - loan_amount
        return emi, total_payment

    def raise_funds(self, ipo_amount, pe_percentage, pe_amount, debt_amount, debt_rate, debt_years, ps_amount):
        self.funds_raised = 0  # Reset funds raised before calculation
        self.fund_sources = {'IPO': 0, 'Private Equity': 0, 'Debt': 0, 'Preference Shares': 0}  # Reset fund sources
        
        remaining_needed = self.project_cost
        
        # Ensure Private Equity does not exceed % limit of project cost
        pe_limit = (pe_percentage / 100) * self.project_cost
        pe_amount = min(pe_amount, pe_limit)
        
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
        
        if self.fund_sources['Debt'] > 0:
            emi, total_payment = self.calculate_debt_emi(self.fund_sources['Debt'], debt_rate, debt_years)
            self.financing_costs['Debt EMI (Monthly)'] = emi
            self.financing_costs['Total Debt Repayment'] = total_payment

    def display_table(self):
        df_funds = pd.DataFrame({'Source': list(self.fund_sources.keys()), 'Funds Raised (INR)': list(self.fund_sources.values())})
        st.write("### Funds Raised Breakdown")
        st.dataframe(df_funds)
        
        df_costs = pd.DataFrame({'Cost Type': list(self.financing_costs.keys()), 'Amount (INR)': list(self.financing_costs.values())})
        st.write("### Financing Costs")
        st.dataframe(df_costs)

st.title("Mining Project Fundraising & Cost Calculator")
company_name = st.text_input("Enter Company Name:")
project_cost = st.number_input("Enter Total Project Cost (INR):", min_value=1.0, format="%.2f")

if "fund_raising" not in st.session_state or st.session_state.fund_raising.company_name != company_name:
    st.session_state.fund_raising = FundRaising(company_name, project_cost)
fund_raising = st.session_state.fund_raising

st.write("## Enter the Maximum Amount You Can Raise from Each Source")
ipo_amount = st.number_input("Maximum IPO Amount (INR):", min_value=0.0, format="%.2f")
pe_percentage = st.number_input("Equity Percentage Offered in Private Equity (%):", min_value=0.0, max_value=100.0, format="%.2f")
pe_amount = st.number_input("Maximum Private Equity Investment (INR):", min_value=0.0, format="%.2f")
debt_amount = st.number_input("Maximum Debt Amount (INR):", min_value=0.0, format="%.2f")
debt_rate = st.number_input("Debt Interest Rate (% per annum):", min_value=0.0, format="%.2f")
debt_years = st.number_input("Debt Tenure (Years):", min_value=1, format="%d")
ps_amount = st.number_input("Maximum Preference Shares Amount (INR):", min_value=0.0, format="%.2f")

if st.button("Calculate Fundraising Plan"):
    fund_raising.raise_funds(ipo_amount, pe_percentage, pe_amount, debt_amount, debt_rate, debt_years, ps_amount)
    st.session_state.fund_raising = fund_raising  # Ensure session state is updated

st.write(f"### Total Funds Raised: {fund_raising.funds_raised:.2f} INR")
remaining_funds = project_cost - fund_raising.funds_raised
if remaining_funds > 0:
    st.write(f"Remaining funds required: {remaining_funds:.2f} INR")
else:
    st.write("Funds raised are sufficient to cover the project cost!")

fund_raising.display_table()
