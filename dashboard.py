import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_bycity_df(df):
    bycity_df = df.groupby(by="customer_city").customer_id.nunique().sort_values(ascending=False).reset_index()
    bycity_df.rename(columns={
        "customer_id": "customer_count"
    }, inplace=True)
    
    return bycity_df

def create_payment_df(df):
    payment_df = df.groupby(by="payment_type").payment_value.sum().sort_values(ascending=False).reset_index()  
    return payment_df

all_df = pd.read_csv("all_data.csv")

datetime_columns = ["order_approved_at", "order_delivered_customer_date"]
all_df.sort_values(by="order_approved_at", inplace=True)
all_df.reset_index(inplace=True)
 
for column in datetime_columns:
    all_df[column] = pd.to_datetime(all_df[column])

min_date = all_df["order_approved_at"].min()
max_date = all_df["order_approved_at"].max()
 
with st.sidebar:
    # Menambahkan logo perusahaan
    st.image("https://companyurlfinder.com/marketing/assets/img/logos/olist.com.png.pagespeed.ce.3oOvWNWNBF.png")
    
    # Mengambil start_date & end_date dari date_input
    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_df = all_df[(all_df["order_approved_at"] >= str(start_date)) & 
                (all_df["order_approved_at"] <= str(end_date))]

bycity_df = create_bycity_df(main_df)
payment_df = create_payment_df(main_df)

st.title('\U0001f6d2 Olist Dashboard \U0001f6d2')

st.subheader('Revenue')

total_revenue = format_currency(main_df.payment_value.sum(), "BRL", locale='es_CO') 
st.metric("Total Revenue", value=total_revenue)

fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(
    main_df["order_approved_at"],
    main_df["payment_value"],
    marker='o', 
    linewidth=2,
    color="#90CAF9"
)
ax.tick_params(axis='y', labelsize=20)
ax.tick_params(axis='x', labelsize=15)
 
st.pyplot(fig)

st.subheader('Most Widely Used Payment Methods')
fig, ax = plt.subplots(figsize=(20, 10))
colors = ["#90CAF9", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="payment_type", 
    y="payment_value",
    data=payment_df.sort_values(by="payment_value", ascending=False),
    palette=colors,
    ax=ax
)
st.pyplot(fig)

st.subheader('Buyers By City')
fig, ax = plt.subplots(figsize=(20, 10))
colors_ = ["#72BCD4", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3", "#D3D3D3"]
sns.barplot(
    x="customer_count", 
    y="customer_city",
    data=bycity_df.head(10).sort_values(by="customer_count", ascending=False),
    palette=colors_
)
st.pyplot(fig)
