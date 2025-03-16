import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import plotly.express as px
from babel.numbers import format_currency
sns.set_theme(style='white')

# helper function
def create_bystate(df):
    bystate = df.groupby(by='customer_state')['customer_id'].nunique().sort_values(ascending=False)
    bystate.rename("number_of_customers", inplace=True)  # Perbaikan disini
    return bystate

def create_bycity(df):
    bycity = df.groupby(by='customer_city')['customer_id'].nunique().sort_values(ascending=False)
    bycity.rename("number_of_customers", inplace=True)  # Perbaikan disini
    return bycity

def create_topProduct(df):
    topProduct = df.groupby(['product_category_name'])['order_item_id'].count().reset_index()
    topProduct = topProduct.sort_values(by='order_item_id', ascending=False).head(10)
    topProduct.rename(columns={'order_item_id':'total_product_sold'}, inplace=True)
    return topProduct

def create_bottomProduct(df):
    bottomProduct = df.groupby(['product_category_name'])['order_item_id'].count().reset_index()
    bottomProduct = bottomProduct.sort_values(by='order_item_id', ascending=True).head(10)
    bottomProduct.rename(columns={'order_item_id':'total_product_sold'}, inplace=True)
    return bottomProduct

def create_monthly_orders(df):
    monthly_orders = df.resample(rule='ME', on='order_purchase_timestamp').agg({
        'order_id':'nunique',
        'price':'sum',
        'customer_id':lambda x: x.nunique()
    }).reset_index()
    monthly_orders.rename(columns={
        'order_purchase_timestamp': 'order_purchase_date',
        'order_id': 'order_count',
        'price': 'revenue',
        'customer_id': 'customer_count'
    }, inplace=True)

    return monthly_orders

# set streamlit page config
st.set_page_config(page_title="Dashboard E-Commerce", page_icon=":convenience_store:", layout="wide")
st.title(":convenience_store: Brazilian E-Commerce Dashboard")
st.markdown('<style>div.block-container{padding-top:2rem;}</style>', unsafe_allow_html=True)

# load the data
file_path ='dashboard/master_orders_2018.csv' 
master_df = pd.read_csv(file_path, encoding='utf-8')

# Convert data types
master_df['order_purchase_timestamp'] = pd.to_datetime(master_df['order_purchase_timestamp'])
master_df.sort_values(by='order_purchase_timestamp', inplace=True)
master_df.reset_index(inplace=True)

# make sidebar for filter by date
with st.sidebar:
    st.title('Filter Data by Date')
    min_date, max_date = master_df['order_purchase_timestamp'].min(), master_df['order_purchase_timestamp'].max()
    start_date, end_date = st.date_input("Date Range", [min_date, max_date], min_value=min_date, max_value=max_date)
    start_date, end_date = pd.to_datetime(start_date), pd.to_datetime(end_date)

# Filter data based on selected date range
main_df = master_df[(master_df['order_purchase_timestamp'] >= start_date) & 
                    (master_df['order_purchase_timestamp'] <= end_date)]

# compute metrics
monthly_orders = create_monthly_orders(main_df)
total_orders = monthly_orders.order_count.sum()
total_revenue = format_currency(monthly_orders.revenue.sum(), 'BRL', locale='pt_BR')
total_customers = monthly_orders.customer_count.sum()

# display  metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric('**✅ Total Orders**', value=total_orders)
with col2:
    st.metric('**💰 Total Revenue**', value=total_revenue)
with col3:
    st.metric('**👥 Total Customers**', value=total_customers)

# Adding spacing
st.markdown("<br>", unsafe_allow_html=True)

# Visualizations orders data
# st.subheader("📈 Number of Order and Revenue by Month")
col1, col2 = st.columns(2)

with col1:
    # plot monthly orders by count order
    st.markdown("<h3 style='text-align: center;'>📈 Number of Orders per Month</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=monthly_orders, x="order_purchase_date", y="order_count", marker="o", color="skyblue", ax=ax)
    ax.set_title("Number of Orders per Month (2018)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Number of Orders")
    plt.xticks(rotation=45)
    st.pyplot(fig)

with col2:
    # plot monthly revenue by revenue
    st.markdown("<h3 style='text-align: center;'>💰 Total Revenue per Month</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.lineplot(data=monthly_orders, x="order_purchase_date", y="revenue", marker="o", color="skyblue", ax=ax)
    ax.set_title("Total Revenue per Month (2018)")
    ax.set_xlabel("Month")
    ax.set_ylabel("Revenue")
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Adding spacing
st.markdown("<br>", unsafe_allow_html=True)

# Visualizations products data
top_products = create_topProduct(main_df)
bottom_products = create_bottomProduct(main_df)

col1, col2 = st.columns(2)
with col1:
    st.markdown("<h3 style='text-align: center;'>🔝 Top 10 Best-Selling Product Categories</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(y=top_products["product_category_name"],
                x=top_products["total_product_sold"], 
                palette="viridis", ax=ax)
    ax.set_title("Top 10 Best-Selling Product Categories", fontsize=12)
    ax.set_xlabel("Total Products Sold")
    ax.set_ylabel("Product Category")
    st.pyplot(fig)

with col2:
    st.markdown("<h3 style='text-align: center;'>🔻 Top 10 Worst-Selling Product Categories</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(y=bottom_products["product_category_name"],
                x=bottom_products["total_product_sold"], 
                palette="magma", ax=ax)
    ax.set_title("Top 10 Worst-Selling Product Categories", fontsize=12)
    ax.set_xlabel("Total Products Sold")
    ax.set_ylabel("Product Category")
    st.pyplot(fig)

# Adding spacing
st.markdown("<br>", unsafe_allow_html=True)

# Visualizations customers data
bystate = create_bystate(main_df)
bycity = create_bycity(main_df)

col1, col2 = st.columns(2)
with col1:
    st.markdown("<h3 style='text-align: center;'>🏢 Top 10 Customer Distribution by State</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(12, 6))
    top_states = bystate.head(10)
    sns.barplot(x=top_states.index, y=top_states.values, palette="Purples_r", ax=ax)
    for p in ax.patches:
        ax.annotate(f"{p.get_height()}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="bottom", fontsize=10)
    ax.grid(False)
    ax.set_title("Top 10 Customer Distribution by State", fontsize=14)
    ax.set_xlabel("State")
    ax.set_ylabel("Number of Customers")
    st.pyplot(fig)

with col2:
    st.markdown("<h3 style='text-align: center;'>🏙️ Top 10 Customer Distribution by City</h3>", unsafe_allow_html=True)
    fig, ax = plt.subplots(figsize=(12, 6))
    top_cities = bycity.head(10)
    sns.barplot(x=top_cities.index, y=top_cities.values, palette="Blues_r", ax=ax)
    for p in ax.patches:
        ax.annotate(f"{p.get_height()}", (p.get_x() + p.get_width() / 2., p.get_height()),
                    ha="center", va="bottom", fontsize=10)
    ax.grid(False)
    ax.set_title("Top 10 Customer Distribution by City", fontsize=14)
    ax.set_xlabel("City")
    ax.set_ylabel("Number of Customers")
    plt.xticks(rotation=45)
    st.pyplot(fig)





