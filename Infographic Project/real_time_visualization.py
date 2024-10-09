import pandas as pd
import plotly.graph_objects as go
import streamlit as st
import mysql.connector
from indicators_for_real_time import *
from query import *


# Create bar chart
def create_bar_chart(data):
    fig = go.Figure(data=go.Bar(x=data['timestamp'], y=data['current_price'], name='Current Price'))
    fig.update_layout(title='Bar Chart of Current Prices', xaxis_title='Timestamp', yaxis_title='Current Price')
    return fig

# Create chart
def create_chart(data, chart_type, indicator=None, window=12):
    if chart_type == "Bar Chart":
        fig = create_bar_chart(data)
    elif chart_type == "Candlestick Chart":
        fig = go.Figure(data=[go.Candlestick(x=data['timestamp'],
                                            open=data['open_price'],
                                            high=data['high_price'],
                                            low=data['low_price'],
                                            close=data['current_price'])])
        fig.update_layout(title='Candlestick Chart', xaxis_title='Timestamp', yaxis_title='Price')
    elif chart_type == "Line Chart":
        fig = go.Figure(data=go.Scatter(x=data['timestamp'], y=data['current_price'], mode='lines', name='Current Price'))
        fig.update_layout(title='Line Chart of Current Prices', xaxis_title='Timestamp', yaxis_title='Current Price')
    elif chart_type == "Area Chart":
        fig = go.Figure(data=go.Scatter(x=data['timestamp'], y=data['current_price'], fill='tozeroy', name='Current Price'))
        fig.update_layout(title='Area Chart of Current Prices', xaxis_title='Timestamp', yaxis_title='Current Price')
    else:
        fig = go.Figure(data=go.Scatter(x=data['timestamp'], y=data['current_price'], mode='lines', name='Current Price'))
        fig.update_layout(title='Default Chart', xaxis_title='Timestamp', yaxis_title='Current Price')

    # Add indicators if specified
    if indicator =="SMA" :
        sma = calculate_sma(data, window=window)
        fig.add_trace(go.Scatter(x=data['timestamp'], y=sma, mode='lines', name=f'SMA ({window})'))
    elif indicator == "EMA":
        ema = calculate_ema(data, window=window)
        fig.add_trace(go.Scatter(x=data['timestamp'], y=ema, mode='lines', name=f'EMA ({window})'))
    elif indicator == "Bollinger Bands":
        sma, upper_band, lower_band = calculate_bollinger_bands(data, window=window)
        fig.add_trace(go.Scatter(x=data['timestamp'], y=upper_band, mode='lines', name=f'Upper Band ({window})'))
        fig.add_trace(go.Scatter(x=data['timestamp'], y=lower_band, mode='lines', name=f'Lower Band ({window})'))
    elif indicator == "Keltner Channels":
        ema_typical_price, upper_channel, lower_channel = calculate_keltner_channels(data, window=window)
        fig.add_trace(go.Scatter(x=data['timestamp'], y=upper_channel, mode='lines', name=f'Upper Keltner Channel ({window})'))
        fig.add_trace(go.Scatter(x=data['timestamp'], y=lower_channel, mode='lines', name=f'Lower Keltner Channel ({window})'))
    elif indicator == "Envelopes":
        upper_envelope, lower_envelope = calculate_envelopes(data, window=window)
        fig.add_trace(go.Scatter(x=data['timestamp'], y=upper_envelope, mode='lines', name=f'Upper Envelope ({window})'))
        fig.add_trace(go.Scatter(x=data['timestamp'], y=lower_envelope, mode='lines', name=f'Lower Envelope ({window})'))
    elif indicator == "Price Channels":
        high_channel, low_channel = calculate_price_channels(data, window=window)
        fig.add_trace(go.Scatter(x=data['timestamp'], y=high_channel, mode='lines', name=f'High Channel ({window})'))
        fig.add_trace(go.Scatter(x=data['timestamp'], y=low_channel, mode='lines', name=f'Low Channel ({window})'))
    elif indicator == "Average True Range (ATR)":
        atr = calculate_atr(data, window=window)
        fig.add_trace(go.Scatter(x=data['timestamp'], y=atr, mode='lines', name=f'ATR ({window})'))

    return fig


def real_time_visualization_ui():
    if st.session_state.get('page') == 'real_time':
        st.title("Real-Time Data Visualization")

        # Define controls for real-time data visualization
        col1, col2 = st.columns(2)

        with col1:
            real_time_chart_type = st.selectbox("Chart Type for Real-Time", ["Bar Chart", "Candlestick Chart", "Line Chart", "Area Chart"])

        with col2:
            indicator = st.selectbox("Indicator", [None, "SMA", "EMA", "Bollinger Bands", "Keltner Channels", "Envelopes", "Average True Range (ATR)", "Price Channels"])

        # Get selected company from the sidebar
        company = st.session_state.get('company')
        
        # Fetch real-time data for the selected company
        real_time_data = fetch_real_time_data(company)

        # Generate and display real-time chart
        real_time_chart = create_chart(real_time_data, real_time_chart_type, indicator)
        st.plotly_chart(real_time_chart, use_container_width=True)


    st.markdown(
    """
    <script>
    function refreshPage() {
        setTimeout(function() {
            window.location.reload();
        }, 300000); // 300000 milliseconds = 5 minutes
    }
    refreshPage();
    </script>
    """,
    unsafe_allow_html=True
)