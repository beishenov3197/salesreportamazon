# Sales Report of Amazon
Python

## Summary 
The analysis focused on Amazon's sales data and encompassed several key areas. 
These included examining sales trends month over month, pinpointing peak sales days, evaluating seasonal patterns, calculating production costs, studying the correlation between product prices and sales, and performing an RFM analysis for customer segmentation.
These insights equip Amazon with valuable information to drive strategic decisions, enhance operational efficiency, and maximize profitability.

## Peak sales days

![image](https://github.com/beishenov3197/salesreportamazon/assets/112967670/38f85ac3-9425-466d-b41d-1428ef3c9259)

- Out of 138 days with sales, the highest daily sales figure exceeded $600,000, while the lowest recorded sales were approximately $4,000. This indicates significant variation in daily sales performance.
- The top-performing sales days stand out considerably from the average daily sales, which hovers around $75,000. These exceptional sales days warrant further investigation and analysis.
- It's crucial to pay close attention to the specific dates that experienced exceptional sales performance and document the underlying reasons. This information will be invaluable for shaping future advertising and marketing strategies.

#### peak_sales_days = sales_data.groupby(sales_data['DATE'].dt.date)['GROSS AMT'].sum()
#### peak_sales_days = peak_sales_days.sort_values(ascending=False)

## Seasonal sales

![Seasons](https://github.com/beishenov3197/salesreportamazon/assets/112967670/bd46aee4-7ab1-4158-8148-a4811273915b)

- Notable growth was observed in October 2021 following a period of recession, although the rate of growth appeared to be slower compared to previous periods.
- The overall trend remained relatively stable without significant fluctuations.
- There was a noticeable decline leading up to October, with a slight recovery followed by a continuous decrease until the end of the observed period.

#### monthly_sales = sales_data.set_index('DATE').resample('M')['GROSS AMT'].sum()
#### stl = STL(monthly_sales, seasonal=13)  # Adjust the seasonal parameter based on your data
#### result = stl.fit()
#### seasonal, trend, residual = result.seasonal, result.trend, result.resid
#### plt.figure(figsize=(12, 6))
#### plt.subplot(311)

## Most and least profitable products

![image](https://github.com/beishenov3197/salesreportamazon/assets/112967670/92603da4-4d70-4e63-8ebe-ccc3f8d65313)

![image](https://github.com/beishenov3197/salesreportamazon/assets/112967670/8107a4f4-93a1-4f24-a728-9daa37b04697)

#### product_profit = sales_data.groupby('SKU')['Cost of Products Sold'].sum() - sales_data.groupby('SKU')['GROSS AMT'].sum()
#### product_profit = product_profit.reset_index()
#### most_profitable_products = product_profit.sort_values(by=0, ascending=False)
#### print("Most Profitable Products:")
#### print(most_profitable_products.head())

#### least_profitable_products = product_profit.sort_values(by=0, ascending=True)

## Monthly sales trends

![Monthly sales](https://github.com/beishenov3197/salesreportamazon/assets/112967670/e439eccb-f0f9-4998-8838-bd217a5d1436)

- Sales follow a standard seasonal trend, rising from June to September, peaking in October, and sharply decreasing until December.
- The month of October stands out as the peak sales period, indicating the importance of focusing marketing and operational efforts during this time.
- After the decline in sales from October to December, there's a subsequent sharp increase, albeit not as significant as the October peak, suggesting potential opportunities for year-end recovery strategies.
