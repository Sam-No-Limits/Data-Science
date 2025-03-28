# -*- coding: utf-8 -*-
"""Facebook-Program.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y7YgDldkgU2Ko-f9r93iZg71FnceLlsN
"""



import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score


facebook_file = "Facebook_Marketplace_data.csv"
sales_file = "advertising_sales_data.xlsx"

if not os.path.exists(facebook_file):
    raise FileNotFoundError(f"Error: {facebook_file} not found. Please check the file path.")

if not os.path.exists(sales_file):
    raise FileNotFoundError(f"Error: {sales_file} not found. Please check the file path.")


facebook_df = pd.read_csv(facebook_file)


facebook_df["status_published"] = pd.to_datetime(facebook_df["status_published"])


plt.figure(figsize=(10, 6))
sns.boxplot(data=facebook_df, x="status_type", y="num_reactions", palette="coolwarm")
plt.title("Distribution of Reactions by Post Type")
plt.xticks(rotation=45)
plt.show()


facebook_df["post_month"] = facebook_df["status_published"].dt.month
monthly_engagement = facebook_df.groupby("post_month")[["num_reactions", "num_comments", "num_shares"]].sum()

plt.figure(figsize=(12, 6))
monthly_engagement.plot(marker="o")
plt.title("Monthly Engagement Trends")
plt.xlabel("Month")
plt.ylabel("Total Engagement")
plt.legend(title="Engagement Type")
plt.grid(True)
plt.show()


sales_df = pd.read_excel(sales_file)


if "Radio" in sales_df.columns:
    sales_df["Radio"] = sales_df["Radio"].fillna(sales_df["Radio"].median())


X = sales_df[["TV", "Radio", "Newspaper"]]
y = sales_df["Sales"]


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = LinearRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)


r2 = r2_score(y_test, y_pred)
rmse = mean_squared_error(y_test, y_pred) ** 0.5

print(f"Model Performance:")
print(f"R² Score: {r2:.3f}")
print(f"Root Mean Squared Error (RMSE): {rmse:.3f}")


coefficients = pd.DataFrame(model.coef_, X.columns, columns=["Coefficient"])
print("\nFeature Importance:")
print(coefficients)