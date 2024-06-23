from flask import Flask, render_template
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.io as pio

app = Flask(__name__)

# Load your data
file_path = 'Pay_slip_excel.xlsx'  # Update this path with your file
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Convert 'Pay slip Date' to datetime
df['Pay slip Date'] = pd.to_datetime(df['Pay slip Date'])

# Calculate totals
total_money_earned = df['Total Pay'].sum()
total_tax_paid = df['Tax Paid'].sum()
total_amount_returned = df['Retured Amount'].sum()
total_in_hand_salary = df['Salary in Hand'].sum()

# Create Plotly figure
fig = make_subplots(
    rows=2, cols=2,
    subplot_titles=("Total Pay", "Tax Paid", 
                    "Salary in Hand", "Proportion of Tax Paid to Total Pay"),
    specs=[[{"type": "bar"}, {"type": "bar"}], 
           [{"type": "bar"}, {"type": "pie"}]],
    vertical_spacing=0.2,  # Adjust vertical spacing between rows
    horizontal_spacing=0.1  # Adjust horizontal spacing between columns
)

# Bar chart for Total Pay over time
fig.add_trace(go.Bar(x=df['Pay slip Date'], y=df['Total Pay'], name='Total Pay', marker_color='blue'), row=1, col=1)

# Bar chart for Tax Paid over time
fig.add_trace(go.Bar(x=df['Pay slip Date'], y=df['Tax Paid'], name='Tax Paid', marker_color='red'), row=1, col=2)

# Bar chart for Salary in Hand over time
fig.add_trace(go.Bar(x=df['Pay slip Date'], y=df['Salary in Hand'], name='Salary in Hand', marker_color='green'), row=2, col=1)

# Pie chart for the proportion of Tax Paid to Total Pay
labels = ['Tax Paid', 'Salary in Hand']
sizes = [total_tax_paid, total_in_hand_salary]

fig.add_trace(go.Pie(labels=labels, values=sizes, hole=.3, name='Proportion of Tax Paid to Total Pay'), row=2, col=2)

# Update layout
fig.update_layout(
    title_text="Salary Data Insights",
    height=700,
    margin=dict(l=50, r=50, b=50, t=80),
    showlegend=False,
    annotations=[dict(
        text="Summary Table",
        showarrow=False,
        xref="paper", yref="paper",
        x=0.5, y=-0.4,
        xanchor='center', yanchor='bottom',
        font=dict(size=14)
    )]
)

# Create summary table as HTML
summary_table = pd.DataFrame({
    "Metric": ["Total Money Earned", "Total Tax Paid", "Total Amount Returned", "Total In-Hand Salary"],
    "Total (CAD$)": [total_money_earned, total_tax_paid, total_amount_returned, total_in_hand_salary]
}).to_html(classes="table table-striped", index=False)

# Home route
@app.route('/')
def index():
    return render_template('index.html', plot_div=pio.to_html(fig, full_html=False), summary_table=summary_table)

if __name__ == '__main__':
    app.run(debug=True)
