import pandas as pd
import plotly.graph_objects as go
from flask import Flask, render_template
import plotly.io as pio
from datetime import datetime, timedelta

app = Flask(__name__)

# Load your data
file_path = 'Pay_slip_excel.xlsx'  # Update this path with your file
df = pd.read_excel(file_path)

# Convert 'Pay slip Date' to datetime
df['Pay slip Date'] = pd.to_datetime(df['Pay slip Date'])

# Sort the dataframe by date
df = df.sort_values('Pay slip Date')

# Extract year from the date
df['Year'] = df['Pay slip Date'].dt.year

# Calculate totals
total_money_earned = df['Total Pay'].sum()
total_tax_paid = df['Tax Paid'].sum()
total_amount_returned = df['Retured Amount'].sum()
total_without_tax = df['total without tax'].sum()

# Function to create year-wise line charts
def create_year_wise_charts(year_df, year):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=year_df['Pay slip Date'], y=year_df['Total Pay'], mode='lines', name='Total Pay', line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=year_df['Pay slip Date'], y=year_df['Tax Paid'], mode='lines', name='Tax Paid', line=dict(color='red')))
    fig.add_trace(go.Scatter(x=year_df['Pay slip Date'], y=year_df['total without tax'], mode='lines', name='Salary Without Tax', line=dict(color='green')))
    fig.update_layout(
        title=f'Pay Slip Analysis for {year}',
        xaxis_title='Date',
        yaxis_title='Amount (CAD$)',
        height=500,  # Increase height for better visibility
        margin=dict(l=50, r=50, b=50, t=80)
    )
    return pio.to_html(fig, full_html=False)

# Create year-wise plots
year_2023_df = df[df['Year'] == 2023]
year_2024_df = df[df['Year'] == 2024]
year_2025_df = df[df['Year'] == 2025]

year_2023_plot = create_year_wise_charts(year_2023_df, 2023)
year_2024_plot = create_year_wise_charts(year_2024_df, 2024)
year_2025_plot = create_year_wise_charts(year_2025_df, 2025)

# Create combined plot for all years
combined_plot = create_year_wise_charts(df, 'All Years')

# Create summary table as HTML
summary_table = pd.DataFrame({
    "Metric": ["Total Money Earned", "Total Tax Paid", "Total Amount Returned", "Total Salary Without Tax"],
    "Total (CAD$)": [total_money_earned, total_tax_paid, total_amount_returned, total_without_tax]
}).to_html(classes="table table-striped", index=False)

# Home route
@app.route('/')
def index():
    return render_template(
        'index.html',
        summary_table=summary_table,
        year_2023_plot=year_2023_plot,
        year_2024_plot=year_2024_plot,
        year_2025_plot=year_2025_plot,
        combined_plot=combined_plot
    )

if __name__ == '__main__':
    app.run(debug=True)