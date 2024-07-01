import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

# Calculate totals
total_money_earned = df['Total Pay'].sum()
total_tax_paid = df['Tax Paid'].sum()
total_amount_returned = df['Retured Amount'].sum()
total_without_tax = df['total without tax'].sum()

# Get current date (for demonstration, let's use the last date in the dataset)
current_date = df['Pay slip Date'].max()

# Calculate earnings for the current month
current_month = df[df['Pay slip Date'].dt.to_period('M') == current_date.to_period('M')]
current_month_total = current_month['Total Pay'].sum()
current_month_tax = current_month['Tax Paid'].sum()
current_month_without_tax = current_month['total without tax'].sum()

# Calculate earnings for the last two weeks
two_weeks_ago = current_date - timedelta(days=14)
last_two_weeks = df[df['Pay slip Date'] >= two_weeks_ago]
last_two_weeks_total = last_two_weeks['Total Pay'].sum()
last_two_weeks_tax = last_two_weeks['Tax Paid'].sum()
last_two_weeks_without_tax = last_two_weeks['total without tax'].sum()

# Create Plotly figure
fig = make_subplots(
    rows=3, cols=2,
    subplot_titles=("Total Pay Over Time", "Tax Paid Over Time",
                    "Salary Without Tax Over Time", "Proportion of Tax Paid to Total Pay",
                    "Current Month Earnings", "Last Two Weeks Earnings"),
    specs=[[{"type": "bar"}, {"type": "bar"}],
           [{"type": "bar"}, {"type": "pie"}],
           [{"type": "pie"}, {"type": "pie"}]],
    vertical_spacing=0.1,
    horizontal_spacing=0.1
)

# Add existing plots
fig.add_trace(go.Bar(x=df['Pay slip Date'], y=df['Total Pay'], name='Total Pay', marker_color='blue'), row=1, col=1)
fig.add_trace(go.Bar(x=df['Pay slip Date'], y=df['Tax Paid'], name='Tax Paid', marker_color='red'), row=1, col=2)
fig.add_trace(go.Bar(x=df['Pay slip Date'], y=df['total without tax'], name='Salary Without Tax', marker_color='green'), row=2, col=1)

# Pie chart for the proportion of Tax Paid to Total Pay
labels = ['Tax Paid', 'Salary Without Tax']
sizes = [total_tax_paid, total_without_tax]
fig.add_trace(go.Pie(labels=labels, values=sizes, hole=.3, name='Proportion of Tax Paid to Total Pay'), row=2, col=2)

# Pie chart for current month earnings
current_month_labels = ['Tax Paid', 'Salary Without Tax']
current_month_sizes = [current_month_tax, current_month_without_tax]
fig.add_trace(go.Pie(labels=current_month_labels, values=current_month_sizes, hole=.3, name='Current Month Earnings'), row=3, col=1)

# Pie chart for last two weeks earnings
last_two_weeks_labels = ['Tax Paid', 'Salary Without Tax']
last_two_weeks_sizes = [last_two_weeks_tax, last_two_weeks_without_tax]
fig.add_trace(go.Pie(labels=last_two_weeks_labels, values=last_two_weeks_sizes, hole=.3, name='Last Two Weeks Earnings'), row=3, col=2)

# Update layout
fig.update_layout(
    height=1000,
    margin=dict(l=50, r=50, b=50, t=80),
    showlegend=False,
    annotations=[dict(
        text="Summary Table",
        showarrow=False,
        xref="paper", yref="paper",
        x=0.5, y=-0.15,
        xanchor='center', yanchor='bottom',
        font=dict(size=14)
    )]
)

# Set x-axis properties to ensure every month is displayed
fig.update_xaxes(tickmode='linear', dtick='M1', tickformat='%b\n%Y', row=1, col=1)
fig.update_xaxes(tickmode='linear', dtick='M1', tickformat='%b\n%Y', row=1, col=2)
fig.update_xaxes(tickmode='linear', dtick='M1', tickformat='%b\n%Y', row=2, col=1)

# Create summary table as HTML
summary_table = pd.DataFrame({
    "Metric": ["Total Money Earned", "Total Tax Paid", "Total Amount Returned", "Total Salary Without Tax"],
    "Total (CAD$)": [total_money_earned, total_tax_paid, total_amount_returned, total_without_tax]
}).to_html(classes="table table-striped", index=False)

# Home route
@app.route('/')
def index():
    return render_template('index.html', plot_div=pio.to_html(fig, full_html=False), summary_table=summary_table)

if __name__ == '__main__':
    app.run(debug=True)
