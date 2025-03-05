import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

def calculate_total_cost(**costs):
    """
    Calculate the total cost estimation dynamically by excluding zero or None values.
    
    Parameters:
    - costs: Keyword arguments representing different cost components.
    
    Returns:
    - The total estimated cost and a breakdown of included costs.
    """
    valid_costs = {key: value for key, value in costs.items() if value not in (None, 0)}
    total_cost = sum(valid_costs.values())
    return total_cost, valid_costs

def plot_cost_distribution(cost_breakdown):
    """
    Generate a pie chart to visualize cost distribution.
    """
    if not cost_breakdown:
        st.warning("No valid costs provided for visualization.")
        return
    
    labels = list(cost_breakdown.keys())
    values = list(cost_breakdown.values())
    
    plt.figure(figsize=(8, 8))
    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=140, colors=plt.cm.Paired.colors)
    plt.title("Cost Breakdown")
    plt.axis('equal')
    st.pyplot(plt)

st.title("Mining Project Cost Estimation Calculator")

# Collecting cost inputs dynamically
st.write("### Enter Cost Components (Leave blank or 0 if not applicable)")
base_cost = st.number_input("Base Cost (INR):", min_value=0.0, format="%.2f")
overhead_cost = st.number_input("Overhead Cost (INR):", min_value=0.0, format="%.2f")
depreciation_cost = st.number_input("Depreciation Cost (INR):", min_value=0.0, format="%.2f")
environmental_cost = st.number_input("Environmental Impact Cost (INR):", min_value=0.0, format="%.2f")
transportation_cost = st.number_input("Transportation Cost (INR):", min_value=0.0, format="%.2f")
labor_cost = st.number_input("Labor Cost (INR):", min_value=0.0, format="%.2f")
material_cost = st.number_input("Material Cost (INR):", min_value=0.0, format="%.2f")
machinery_cost = st.number_input("Machinery Cost (INR):", min_value=0.0, format="%.2f")
fuel_cost = st.number_input("Fuel Cost (INR):", min_value=0.0, format="%.2f")
maintenance_cost = st.number_input("Maintenance Cost (INR):", min_value=0.0, format="%.2f")

# Handling dynamic variable costs
variable_costs = []
num_variable_costs = st.number_input("Number of additional variable costs:", min_value=0, max_value=20, step=1)
for i in range(int(num_variable_costs)):
    variable_costs.append(st.number_input(f"Enter Variable Cost {i+1} (INR):", min_value=0.0, format="%.2f"))

if st.button("Calculate Total Cost"):
    total_cost, cost_breakdown = calculate_total_cost(
        base_cost=base_cost,
        overhead_cost=overhead_cost,
        depreciation_cost=depreciation_cost,
        environmental_cost=environmental_cost,
        transportation_cost=transportation_cost,
        labor_cost=labor_cost,
        material_cost=material_cost,
        machinery_cost=machinery_cost,
        fuel_cost=fuel_cost,
        maintenance_cost=maintenance_cost,
        **{f"Variable Cost {i+1}": cost for i, cost in enumerate(variable_costs) if cost > 0}
    )
    
    st.write(f"## Total Estimated Cost: {total_cost:.2f} INR")
    
    # Display cost breakdown
    if cost_breakdown:
        df = pd.DataFrame(list(cost_breakdown.items()), columns=["Cost Component", "Amount (INR)"])
        st.dataframe(df)
        plot_cost_distribution(cost_breakdown)
