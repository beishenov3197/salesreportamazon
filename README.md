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
