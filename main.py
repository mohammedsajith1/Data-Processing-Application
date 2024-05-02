import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from abc import ABC, abstractmethod

# Set page config
st.set_page_config(page_title="Comprehensive Data Processing Application", layout="wide")

class DataIngestionProcess(ABC):
    @abstractmethod
    def load_data(self, file):
        pass

    @abstractmethod
    def clean_data(self, data):
        pass

class FinanceDataIngestion(DataIngestionProcess):
    def load_data(self, file):
        data = pd.read_csv(file)
        data.columns = data.columns.str.strip().str.lower().str.replace(' ', '_')
        return data

    def clean_data(self, data):
        currency_cols = ['units_sold', 'manufacturing_price', 'sale_price', 'gross_sales', 'discounts', 'sales', 'cogs', 'profit']
        for col in currency_cols:
            if col in data.columns:
                data[col] = data[col].astype(str).str.replace(r'[\$,]', '', regex=True).str.strip().replace('', 'NaN')
                data[col] = pd.to_numeric(data[col], errors='coerce')
        data['date'] = pd.to_datetime(data['date'], errors='coerce')
        return data

class SalesDataIngestion(DataIngestionProcess):
    def load_data(self, file):
        data = pd.read_csv(file)
        return data

    def clean_data(self, data):
        data['Order Date'] = pd.to_datetime(data['Order Date'])
        data['Profit'] = (data['Price Each'] - data.get('Cost price', data['Price Each'])) * data['Quantity Ordered']
        return data

class PurchasePriceDataIngestion(DataIngestionProcess):
    def load_data(self, file):
        data = pd.read_csv(file)
        return data

    def clean_data(self, data):
        if 'Volume' in data.columns:
            data['Volume_ml'] = pd.to_numeric(data['Volume'].astype(str).str.extract(r'(\d+)')[0], errors='coerce')
        if 'Size' in data.columns:
            data['Size_ml'] = pd.to_numeric(data['Size'].astype(str).str.extract(r'(\d+)')[0], errors='coerce')
        data.drop_duplicates(inplace=True)
        numeric_cols = data.select_dtypes(include=[np.number]).columns.tolist()
        for col in numeric_cols:
            data[col] = data[col].fillna(data[col].mean())
        return data
    
# main.py

def integrate_with_erp(data):
    # Placeholder for ERP integration logic
    return True


# Main function for Streamlit app
def main():
    st.title("Comprehensive Data Processing Application")
    st.sidebar.title("Upload Data Section")

    # Upload fields for each data type
    uploaded_file_finance = st.sidebar.file_uploader("Upload Finance Data", type=['csv'], key='finance')
    uploaded_file_sales = st.sidebar.file_uploader("Upload Sales Data", type=['csv'], key='sales')
    uploaded_file_purchase = st.sidebar.file_uploader("Upload Purchase Price Data", type=['csv'], key='purchase')

    # Processing Finance Data
    if uploaded_file_finance is not None:
        try:
            finance_data_ingestion = FinanceDataIngestion()
            df_finance = finance_data_ingestion.load_data(uploaded_file_finance)
            df_finance_clean = finance_data_ingestion.clean_data(df_finance)
            show_finance_data(df_finance_clean)
        except Exception as e:
            st.error(f"An error occurred with the finance data: {e}")

    # Processing Sales Data
    if uploaded_file_sales is not None:
        try:
            sales_data_ingestion = SalesDataIngestion()
            df_sales = sales_data_ingestion.load_data(uploaded_file_sales)
            df_sales_clean = sales_data_ingestion.clean_data(df_sales)
            show_sales_data(df_sales_clean)
        except Exception as e:
            st.error(f"An error occurred with the sales data: {e}")

    # Processing Purchase Price Data
    if uploaded_file_purchase is not None:
        try:
            purchase_data_ingestion = PurchasePriceDataIngestion()
            df_purchase = purchase_data_ingestion.load_data(uploaded_file_purchase)
            df_purchase_clean = purchase_data_ingestion.clean_data(df_purchase)
            show_purchase_data(df_purchase_clean)
        except Exception as e:
            st.error(f"An error occurred with the purchase price data: {e}")

def show_finance_data(df):
    st.write("### Finance Data Overview")
    st.dataframe(df.head())
    st.write(df.describe())
    plot_finance_data(df)

def show_sales_data(df):
    st.write("### Sales Data Overview")
    st.dataframe(df.head())
    summary_df = pd.DataFrame({
        "Metric": ["Total Sales", "Average Sales Price", "Max Sale", "Min Sale", "Total Quantity Sold", "Total Profit"],
        "Value": [
            df['Price Each'].sum(),
            df['Price Each'].mean(),
            df['Price Each'].max(),
            df['Price Each'].min(),
            df['Quantity Ordered'].sum(),
            df['Profit'].sum()
        ]
    })
    st.write(summary_df)
    plot_sales_data(df)

def show_purchase_data(df):
    st.write("### Purchase Price Data Overview")
    st.dataframe(df.head())
    plot_purchase_price_data(df)

def plot_finance_data(df):
    st.subheader("Sales by Product")
    fig = px.bar(df.groupby('product')['sales'].sum().reset_index(), x='product', y='sales',
                 title="Sales by Product", labels={'sales': 'Total Sales', 'product': 'Product'})
    fig.update_layout(xaxis_title="Product", yaxis_title="Total Sales", xaxis={'categoryorder':'total descending'})
    st.plotly_chart(fig)

    st.subheader("Profit Over Time")
    df['date'] = pd.to_datetime(df['date'])  # Ensure date is in datetime format
    df_resampled = df.set_index('date')['profit'].resample('M').sum().reset_index()
    fig = px.line(df_resampled, x='date', y='profit', title='Profit Over Time', labels={'profit': 'Total Profit'})
    st.plotly_chart(fig)

def plot_sales_data(df):
    st.subheader("Monthly Profit Analysis")
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    df['Month'] = df['Order Date'].dt.to_period('M')
    monthly_profit = df.groupby('Month')['Profit'].sum().reset_index()
    monthly_profit['Month'] = monthly_profit['Month'].astype(str)  # Convert period to string for plotting
    fig = px.line(monthly_profit, x='Month', y='Profit', title='Monthly Profit Over Time', labels={'Profit': 'Total Profit', 'Month': 'Month'})
    fig.update_xaxes(tickangle=45)
    st.plotly_chart(fig)

def plot_purchase_price_data(data):
    # Check if columns required for plotting are present
    if 'PurchasePrice' not in data.columns or 'Price' not in data.columns or 'Classification' not in data.columns:
        raise ValueError("Data does not have the required columns for plotting purchase price data")

    # Plot Price vs Purchase Price comparison
    try:
        fig = px.scatter(
            data,
            x='PurchasePrice',
            y='Price',
            color='Classification',
            labels={'Price': 'Sale Price', 'PurchasePrice': 'Purchase Price'},
            title='Purchase Price vs. Sale Price by Classification'
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error plotting Price vs Purchase Price: {e}")

    # Plot Distribution of Purchase Prices
    try:
        fig = px.histogram(data, x='PurchasePrice', nbins=30, title='Distribution of Purchase Prices')
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error plotting Distribution of Purchase Prices: {e}")

    # Plot Bar chart of Average Prices by Vendor
    try:
        avg_prices = data.groupby('VendorName')['Price'].mean().reset_index()
        fig = px.bar(
            avg_prices,
            x='VendorName',
            y='Price',
            labels={'Price': 'Average Sale Price', 'VendorName': 'Vendor'},
            title='Average Sale Price by Vendor',
            orientation='v'
        )
        fig.update_layout(
            xaxis={'categoryorder': 'total descending'},
            xaxis_title="Vendor",
            yaxis_title="Average Sale Price ($)"
        )
        st.plotly_chart(fig)
    except Exception as e:
        st.error(f"Error plotting Average Prices by Vendor: {e}")


if __name__ == "__main__":
    main()






