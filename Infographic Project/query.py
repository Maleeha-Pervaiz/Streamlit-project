import mysql.connector 
import streamlit as st
import pandas as pd



#connection 

conn=mysql.connector.connect(
    host="localhost",
    port="3306",
    user="root",
    password="hello",
    database="infographic_db"
)

c=conn.cursor()

#fetch

def view_all_data():
    c.execute('SELECT * FROM historical_data ORDER BY date ASC')
    data = c.fetchall()
    return data



def fetch_real_time_data(selected_company):
    c = conn.cursor()
    query = """
    SELECT stock_symbol, timestamp, open_price, high_price, low_price, current_price, volume
    FROM real_time_data
    WHERE stock_symbol = %s
    """
    c.execute(query, (selected_company,))
    data = c.fetchall()
    # Convert to DataFrame
    df = pd.DataFrame(data, columns=['stock_symbol', 'timestamp', 'open_price', 'high_price', 'low_price', 'current_price', 'volume'])
    return df