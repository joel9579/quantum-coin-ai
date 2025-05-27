import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
import numpy as np

# Load CSV data
df = pd.read_csv("C:\\Users\\mugesh\\Downloads\\Project - Joel\\crypto-forecast-app\\static\\reports\\forecast\\coin_Bitcoin_forecast.csv", parse_dates=['ds'])
df = df.sort_values('ds')
df.set_index('ds', inplace=True)

# Resample to monthly mean
monthly = df['yhat'].resample('M').mean()

# 1. Forecast Trend Line using Linear Regression
monthly = monthly.dropna()
X = np.arange(len(monthly)).reshape(-1, 1)
y = monthly.values
model = LinearRegression()
model.fit(X, y)
forecast = model.predict(X)

plt.figure(figsize=(10, 6))
plt.plot(monthly.index, y, label='Actual')
plt.plot(monthly.index, forecast, label='Trend Line (Forecast)', linestyle='--')
plt.title('Forecast Trend Line')
plt.xlabel('Date')
plt.ylabel('Forecasted Price (yhat)')
plt.legend()
plt.grid()
plt.show()

# 2. Yearly Forecast Summary (mean yhat per year)
yearly_summary = df['yhat'].resample('Y').mean()
plt.figure(figsize=(8, 5))
yearly_summary.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title('Yearly Forecast Summary (Average yhat)')
plt.xlabel('Year')
plt.ylabel('Average Forecasted Price')
plt.xticks(rotation=45)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()


# 3. Correlation Matrix (yhat, yhat_lower, yhat_upper)
numeric_df = df[['yhat', 'yhat_lower', 'yhat_upper']]
correlation = numeric_df.corr()

plt.figure(figsize=(8, 6))
sns.heatmap(correlation, annot=True, cmap='coolwarm', linewidths=0.5, vmin=-1, vmax=1)
plt.title('Correlation Matrix of Forecast Metrics')
plt.tight_layout()
plt.show()



