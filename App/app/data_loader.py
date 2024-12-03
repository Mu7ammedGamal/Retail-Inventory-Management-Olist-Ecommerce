import pyodbc
import pandas as pd
from config import Config
from sqlalchemy import create_engine
import urllib

olist = pd.read_csv("app/preprocessed_data.csv")
olist_data = olist[:5]

def load_olist_data():
    return olist_data

def load_data():
    connection_string = Config.SQLALCHEMY_DATABASE_URI.replace('mssql+pyodbc:///?odbc_connect=','')
    conn = pyodbc.connect(connection_string)
    # Encode the connection string properly for SQLAlchemy
    
    customer_query = 'select Top 5 customer_id from customers'
    geolocation_query = 'select * from geolocation'
    orderitem_query = 'select * from order_items'
    payment_query = 'select * from payments'
    review_query = 'select * from reviews'
    order_query = 'select * from orders'
    product_query = 'select * from products'
    seller_query = 'select * from sellers'
    
    df_customers = pd.read_sql(customer_query,conn)
    df_geolocation = pd.read_sql(geolocation_query,conn)
    df_orderitem = pd.read_sql(orderitem_query,conn)
    df_payment = pd.read_sql(payment_query,conn)
    df_reviews = pd.read_sql(review_query,conn)
    df_orders = pd.read_sql(order_query,conn)
    df_products = pd.read_sql(product_query,conn)
    df_seller = pd.read_sql(seller_query,conn)

    #renaming all the zip_code_prefix so as to make the name common in all tables inorder to perform join

    df_geolocation.rename(columns={'geolocation_zip_code':'zip_code_prefix'},inplace=True)
    df_customers.rename(columns={'customer_zip_code':'zip_code_prefix'},inplace=True)
    df_seller.rename(columns={'seller_zip_code':'zip_code_prefix'},inplace=True)

    #A = pd.merge(df_orders,df_reviews,on='order_id')
    #A = pd.merge(A,df_payment,on='order_id')
    #A = pd.merge(A,df_customers,on='customer_id')
    #peforming left outer join as we need every geo based address related to customer
    #A = pd.merge(A,df_geolocation,how='left',on='zip_code_prefix')

    #merging all seller related data

    #B = pd.merge(df_orderitem,df_products,on='product_id')
    #B = pd.merge(B,df_seller,on='seller_id')
    #peforming left outer join as we need every geo based address related to seller
    #B = pd.merge(B,df_geolocation,how='left',on='zip_code_prefix')

    #data = pd.merge(A,B,on='order_id')

    df_customers = df_customers[:5]
    df_geolocation = df_geolocation[:5]
    df_orderitem = df_orderitem[:5]
    df_payment = df_payment[:5]
    df_reviews = df_reviews[:5]
    df_orders = df_orders[:5]
    df_products = df_products[:5]
    df_seller = df_seller[:5]

    print("Dataframe Loaded Successfully")

    return df_customers,df_geolocation,df_orderitem,df_payment,df_reviews,df_orders,df_products,df_seller,olist_data