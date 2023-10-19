import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.seasonal import STL
from statsmodels.tsa.arima_model import ARIMA
import plotly.express as px

sales_data = pd.read_csv("C:/Users/user/Documents/E-commerce sales dataset/International sale Report.csv")
# Display the first few rows to understand the data structure
print(sales_data.head())
print(sales_data.info())
print(sales_data.describe())

# Convert DATE column to datetime format
sales_data['DATE'] = pd.to_datetime(sales_data['DATE'], format='%m-%d-%y', errors='coerce')
sales_data['PCS'] = sales_data['PCS'].astype(float)
sales_data['RATE'] = sales_data['RATE'].str.replace(',', '').astype(float)  # Remove commas and convert to float
sales_data['GROSS AMT'] = sales_data['GROSS AMT'].str.replace(',', '').astype(float)
sales_data.dropna(subset=['DATE', 'CUSTOMER', 'Months', 'Style', 'SKU', 'Size', 'PCS', 'RATE', 'GROSS AMT'], inplace=True)

# Check data types and basic statistics
print(sales_data.info())
print(sales_data.describe())
duplicates = sales_data.duplicated().sum()
print(f"Duplicate rows: {duplicates}")
print(sales_data['Months'].unique())

# Filter data for a specific month (e.g., June 2021)
june_sales = sales_data[sales_data['DATE'].dt.month == 6]
total_sales_revenue = june_sales['GROSS AMT'].sum()
print(f"Total sales revenue for June 2021: ${total_sales_revenue:.2f}")

# Group data by SKU and calculate total quantity sold
top_selling_products = sales_data.groupby('SKU')['PCS'].sum().reset_index()
top_selling_products = top_selling_products.sort_values(by='PCS', ascending=False)
print("Top-Selling Products:")
print(top_selling_products.head())
top_selling_products.to_csv("top_selling_products.csv", index=False)

# Analyze peak sales days
peak_sales_days = sales_data.groupby(sales_data['DATE'].dt.date)['GROSS AMT'].sum()
peak_sales_days = peak_sales_days.sort_values(ascending=False)
print("Peak Sales Days:")
print(peak_sales_days.head())
peak_sales_days.to_csv("peak_sales_days.csv")

#Seasonal component
monthly_sales = sales_data.set_index('DATE').resample('M')['GROSS AMT'].sum()
stl = STL(monthly_sales, seasonal=13)  # Adjust the seasonal parameter based on your data
result = stl.fit()
seasonal, trend, residual = result.seasonal, result.trend, result.resid
plt.figure(figsize=(12, 6))
plt.subplot(311)
plt.plot(seasonal)
plt.title('Seasonal Component')
plt.subplot(312)
plt.plot(trend)
plt.title('Trend Component')
plt.subplot(313)
plt.plot(residual)
plt.title('Residual Component')
plt.tight_layout()
plt.show()

# Calculate the cost of products sold for each transaction
sales_data['Cost of Products Sold'] = sales_data['PCS'] * sales_data['RATE']
total_cost_of_products_sold = sales_data['Cost of Products Sold'].sum()
print(f"Total cost of products sold: ${total_cost_of_products_sold:.2f}")
total_profit = total_sales_revenue - total_cost_of_products_sold
print(f"Total profit: ${total_profit:.2f}")
profit_margin = (total_profit / total_sales_revenue) * 100  # Convert to a percentage
print(f"Profit margin: {profit_margin:.2f}%")

# Group data by SKU and calculate total profit for each product
product_profit = sales_data.groupby('SKU')['Cost of Products Sold'].sum() - sales_data.groupby('SKU')['GROSS AMT'].sum()
product_profit = product_profit.reset_index()
most_profitable_products = product_profit.sort_values(by=0, ascending=False)
print("Most Profitable Products:")
print(most_profitable_products.head())
least_profitable_products = product_profit.sort_values(by=0, ascending=True)
print("Least Profitable Products:")
print(least_profitable_products.head())
most_profitable_products.to_csv("Most_Profitable_Products.csv")
least_profitable_products.to_csv("Least_Profitable_Products.csv")

# Create a time series plot of monthly sales
monthly_sales = sales_data.set_index('DATE').resample('M')['GROSS AMT'].sum()
monthly_sales.plot(figsize=(12, 6))
plt.title('Monthly Sales Trends')
plt.xlabel('Date')
plt.ylabel('Sales Amount')
plt.grid()
plt.show()

# Create a scatter plot to analyze the relationship between product price and sales
plt.figure(figsize=(10, 6))
plt.scatter(sales_data['RATE'], sales_data['GROSS AMT'], alpha=0.5)
plt.title('Product Price vs. Sales')
plt.xlabel('Product Price')
plt.ylabel('Sales Amount')
plt.grid()
plt.show()

# Create a pivot table to identify frequently co-occurring SKUs
co_occurrence_matrix = sales_data.pivot_table(index='index', columns='SKU', values='PCS', fill_value=0)
co_occurrence_matrix = co_occurrence_matrix.T.dot(co_occurrence_matrix)
frequent_co_occurring_SKUs = co_occurrence_matrix.where(co_occurrence_matrix > 0).stack()
frequent_co_occurring_SKUs = frequent_co_occurring_SKUs.reset_index()
frequent_co_occurring_SKUs.columns = ['SKU1', 'SKU2', 'Frequency']
frequent_co_occurring_SKUs = frequent_co_occurring_SKUs.sort_values(by='Frequency', ascending=False)
print("Frequently Co-occurring SKUs:")
print(frequent_co_occurring_SKUs.head())
frequent_co_occurring_SKUs.to_csv("Frequent_co_occurrence_SKUs.csv")

# Calculate Recency, Frequency, and Monetary Value for each customer
today = pd.to_datetime('today')
customer_rfm = sales_data.groupby('CUSTOMER').agg({
    'DATE': lambda x: (today - x.max()).days,
    'index': 'count',
    'GROSS AMT': 'sum'
})
customer_rfm.columns = ['Recency', 'Frequency', 'Monetary']
# Calculate quartiles for RFM values
quartiles = customer_rfm.quantile([0.25, 0.5, 0.75])
# Define segmentation criteria based on quartiles
def rfm_segment(row):
    if row['Recency'] <= quartiles['Recency'][0.25]:
        return 'Low Recency'
    elif row['Recency'] <= quartiles['Recency'][0.5]:
        return 'Medium Recency'
    else:
        return 'High Recency'
def f_segment(row):
    if row['Frequency'] <= quartiles['Frequency'][0.25]:
        return 'Low Frequency'
    elif row['Frequency'] <= quartiles['Frequency'][0.5]:
        return 'Medium Frequency'
    else:
        return 'High Frequency'
def m_segment(row):
    if row['Monetary'] <= quartiles['Monetary'][0.25]:
        return 'Low Monetary'
    elif row['Monetary'] <= quartiles['Monetary'][0.5]:
        return 'Medium Monetary'
    else:
        return 'High Monetary'
customer_rfm['R_Segment'] = customer_rfm.apply(rfm_segment, axis=1)
customer_rfm['F_Segment'] = customer_rfm.apply(f_segment, axis=1)
customer_rfm['M_Segment'] = customer_rfm.apply(m_segment, axis=1)
# Analyze high-value customers (High Monetary segment)
high_monetary_segment = customer_rfm[customer_rfm['M_Segment'] == 'High Monetary']
# Calculate the average monetary value for high-value customers
average_monetary_value = high_monetary_segment['Monetary'].mean()
print(f"Average Monetary Value for High-Value Customers: ${average_monetary_value:.2f}")
# Calculate metrics for each segment
segment_metrics = rfm_segments.agg({
    'Recency': 'mean',
    'Frequency': 'mean',
    'Monetary': 'mean'
}).reset_index()
# Rename columns for clarity
segment_metrics.columns = ['R_Segment', 'F_Segment', 'M_Segment', 'Average Recency', 'Average Frequency', 'Average Monetary']
# Sort segments by monetary value in descending order
segment_metrics = segment_metrics.sort_values(by='Average Monetary', ascending=False)
# Display all segments and their characteristics
print("Segment Analysis:")
print(segment_metrics)
segment_metrics.to_csv("RFM.csv")

fig = px.line(monthly_sales, title='Interactive Sales Trends Over Time')
fig.update_xaxes(title_text='Date')
fig.update_yaxes(title_text='Sales Amount')
fig.show()
fig = px.scatter(sales_data, x='RATE', y='GROSS AMT', title='Interactive Product Price vs. Sales')
fig.update_traces(marker=dict(size=5))
fig.update_xaxes(title_text='Product Price')
fig.update_yaxes(title_text='Sales Amount')
fig.show()
fig = px.bar(segment_metrics, x='M_Segment', y='Average Monetary', title='Interactive Customer Segmentation Analysis')
fig.update_xaxes(title_text='Monetary Segment')
fig.update_yaxes(title_text='Average Monetary Value')
fig.show()

# Define a function to adjust prices
def adjust_prices(df, adjustment_factor):
    df['Adjusted Price'] = df['RATE'] * (1 + adjustment_factor)
    return df
adjustment_factor = 0.10
sales_data = adjust_prices(sales_data, adjustment_factor)
sales_data.to_csv("adjusted_sales_data.csv", index=False)

# Calculate product demand (example: frequency of purchase)
product_demand = sales_data.groupby('SKU')['index'].count().reset_index()
product_demand.columns = ['SKU', 'Demand']
low_demand_threshold = 10
low_demand_products = product_demand[product_demand['Demand'] < low_demand_threshold]
for sku in low_demand_products['SKU']:
    # Implement inventory reduction strategy for low-demand products
    # For example, reduce order quantities or consider discontinuation
low_demand_products.to_csv("low_demand_products.csv", index=False)


# Simulated customer data (you can replace this with your actual customer data)
customer_data = pd.DataFrame({
    'Customer ID': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'Recency': [20, 50, 10, 60, 5, 35, 70, 25, 45, 15],  # Replace with actual recency values
    'Frequency': [5, 2, 8, 1, 10, 3, 1, 6, 4, 9],  # Replace with actual frequency values
    'Monetary': [1000, 500, 2000, 250, 3000, 800, 150, 1200, 600, 1800]  # Replace with actual monetary values
})

# Define marketing strategies based on RFM segments
marketing_strategies = {
    "High Recency": "Send a personalized email to high recency customers with a special discount code for their next purchase. Highlight new arrivals or bestsellers.",
    "Medium Recency": "Send a targeted email to medium recency customers, featuring product recommendations based on their previous purchases. Encourage them to explore more products.",
    "Low Recency": "Re-engage low recency customers with a win-back campaign. Offer a time-limited discount or a loyalty program to entice them to make a new purchase."
}

# Perform customer segmentation based on Recency
def segment_customers(row):
    return "High Recency" if row['Recency'] <= 10 else "Medium Recency" if row['Recency'] <= 30 else "Low Recency"

customer_data['Segment'] = customer_data.apply(segment_customers, axis=1)

# Iterate through customer segments and apply the respective marketing strategy
for segment, strategy in marketing_strategies.items():
    # Get the list of customers in the current segment
    customers_in_segment = customer_data[customer_data['Segment'] == segment]['Customer ID'].tolist()
    
    # Implement the marketing strategy for customers in this segment
    for customer_id in customers_in_segment:
        # Send the recommended marketing message to each customer
        # This could be via email, targeted ads, or other marketing channels
        print(f"Sending marketing message to customer ID {customer_id} in the {segment} segment:")
        print(strategy)
        print("\n")
