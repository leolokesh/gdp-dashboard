import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Sample Data
sample_data = [
    {
        'TransactionID': 'T0001', 'Date': '2023-01-01', 'StoreID': 'S001', 'SKU_ID': 'P001', 'QuantitySold': 5,
        'UnitPrice': 50, 'Revenue': 250, 'PromotionID': 'PR001', 'PromotionType': 'Discount', 'FootTrafficCount': 250,
        'CurrentStockLevel': 15, 'RestockDate': '2023-01-06', 'LastRestockDate': '2022-12-30', 'StockoutDays': 0,
        'SupplierID': 'SUP001', 'SupplierName': 'Supplier A', 'LeadTime': '5 days', 'StockoutRiskScore': 0.85,
        'RecommendedRestockQuantity': 50, 'RecommendedRestockDate': '2023-01-04', 'ClusterID': 'C1',
        'PerformanceIssue': 'Low Conversion Rate', 'AnomalyFlag': 0, 'AnomalyType': '',
    },
    # ... add the remaining data here
]

# Convert to pandas DataFrame
df = pd.DataFrame(sample_data)

# Function to process stockout risk data
def process_stockout_risk_data(df):
    grouped_data = df.groupby('SKU_ID').agg({'StockoutRiskScore': 'mean'}).reset_index()
    grouped_data.columns = ['SKU_ID', 'AverageRisk']
    return grouped_data

# Function to process sales trend data
def process_sales_trend_data(df):
    grouped_data = df.groupby('Date').agg({'Revenue': 'sum', 'QuantitySold': 'sum'}).reset_index()
    return grouped_data

# Function to process cluster analysis data
def process_cluster_data(df):
    cluster_data = df[['FootTrafficCount', 'Revenue', 'QuantitySold', 'ClusterID']]
    return cluster_data

# Streamlit Sidebar
st.sidebar.title("Walkaroo Sales Dashboard")
graph_choice = st.sidebar.radio("Choose Graph:", 
                                ['Stockout Risk', 'Sales Trend', 'Cluster Analysis'])

# Main Area based on user selection
if graph_choice == 'Stockout Risk':
    st.header("Predictive Stockout Risk Model")
    stockout_data = process_stockout_risk_data(df)
    
    fig = px.bar(stockout_data, x='SKU_ID', y='AverageRisk', 
                 title="Stockout Risk by SKU", 
                 labels={'AverageRisk': 'Stockout Risk Score'},
                 color='AverageRisk',
                 color_continuous_scale=px.colors.sequential.Viridis)
    st.plotly_chart(fig)

elif graph_choice == 'Sales Trend':
    st.header("Sales Trend Analysis")
    sales_trend_data = process_sales_trend_data(df)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=sales_trend_data['Date'], y=sales_trend_data['Revenue'], 
                             mode='lines+markers', name='Revenue'))
    fig.add_trace(go.Scatter(x=sales_trend_data['Date'], y=sales_trend_data['QuantitySold'], 
                             mode='lines+markers', name='Quantity Sold'))
    fig.update_layout(title="Sales Trend Over Time", xaxis_title='Date', yaxis_title='Amount')
    st.plotly_chart(fig)

elif graph_choice == 'Cluster Analysis':
    st.header("Root Cause Analysis via Clustering")
    cluster_data = process_cluster_data(df)
    
    fig = px.scatter(cluster_data, x='FootTrafficCount', y='Revenue', 
                     size='QuantitySold', color='ClusterID', 
                     title="Cluster Analysis", hover_data=['ClusterID'])
    st.plotly_chart(fig)

# Insights Section
st.subheader("Overall Insights & Suggestions")
st.markdown("""
- **Optimize Stock for High-Traffic Stores**: Cluster C1 (S001, S003, S005) needs stock prioritization to capture sales opportunities.
- **Prevent Stockouts Proactively**: Monitor real-time inventory to avoid high stockout risks for products like P007.
- **Improve Marketing for Low Conversions**: Enhance marketing and product positioning for stores in Cluster C1 to boost conversion rates.
""")
