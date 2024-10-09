import streamlit as st
import pandas as pd
from real_time_visualization import real_time_visualization_ui
import plotly.graph_objs as go
from chart_utils import *
from indicator_utils import *
from query import *
from style_config import configure_streamlit, apply_custom_css
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.units import inch
import pandas as pd
import sqlite3
import mysql.connector 
import plotly.graph_objects as go
import kaleido 
from comparison_utils import create_comparison_chart
# Fetch data from the database
results = view_all_data()

# Convert the results to a DataFrame
df = pd.DataFrame(results, columns=["stock_symbol", "date", "open_price", "high_price", "low_price", "close_price", "volume"])

# Ensure the date column is in datetime format
df['date'] = pd.to_datetime(df['date'])

# Set a common height and width for all charts
chart_height = 600
chart_width = 1000

# Define range selector buttons including the new options
rangeselector_buttons = [
    dict(count=5, label="5D", step="day", stepmode="backward"),
    dict(count=1, label="1M", step="month", stepmode="backward"),
    dict(count=3, label="3M", step="month", stepmode="backward"),
    dict(label="YTD", step="year", stepmode="todate"),
    dict(count=1, label="1Y", step="year", stepmode="backward"),
    dict(count=3, label="3Y", step="year", stepmode="backward"),
    dict(count=5, label="5Y", step="year", stepmode="backward"),
    dict(step="all")
]

# Define grid settings for xaxis and yaxis
axis_config = dict(
    gridcolor='rgb(200, 200, 200)',  # Set grid line color
    gridwidth=1,  # Set grid line width
    tickformat='%Y-%m-%d',  # Format tick marks for xaxis
    tickformat_y='.2f'  # Format tick marks for yaxis
)

# Function to create different types of charts with optional indicators
def create_chart(data, chart_type, indicator=None, window=20):
    if chart_type == "Candlestick Chart":
        fig = create_candlestick_chart(data, company)
    elif chart_type == "Line Chart":
        fig = create_line_chart(data)
    elif chart_type == "Bar Chart":
        fig = create_bar_chart(data)
    elif chart_type == "Area Chart":
        fig = create_area_chart(data)

    # Add indicator if selected
    if indicator == "SMA":
        sma = calculate_sma(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=sma, mode='lines', name=f'SMA ({window})'))
    elif indicator == "EMA":
        ema = calculate_ema(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=ema, mode='lines', name=f'EMA ({window})'))
    elif indicator == "Bollinger Bands":
        sma, upper_band, lower_band = calculate_bollinger_bands(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=upper_band, mode='lines', name=f'Upper Band ({window})'))
        fig.add_trace(go.Scatter(x=data['date'], y=lower_band, mode='lines', name=f'Lower Band ({window})'))
    elif indicator == "Keltner Channels":
        ema_typical_price, upper_channel, lower_channel = calculate_keltner_channels(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=upper_channel, mode='lines', name=f'Upper Keltner Channel ({window})'))
        fig.add_trace(go.Scatter(x=data['date'], y=lower_channel, mode='lines', name=f'Lower Keltner Channel ({window})'))
    elif indicator == "Envelopes":
        upper_envelope, lower_envelope = calculate_envelopes(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=upper_envelope, mode='lines', name=f'Upper Envelope ({window})'))
        fig.add_trace(go.Scatter(x=data['date'], y=lower_envelope, mode='lines', name=f'Lower Envelope ({window})'))
    elif indicator == "Price Channels":
        high_channel, low_channel = calculate_price_channels(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=high_channel, mode='lines', name=f'High Channel ({window})'))
        fig.add_trace(go.Scatter(x=data['date'], y=low_channel, mode='lines', name=f'Low Channel ({window})'))
    elif indicator == "Average True Range (ATR)":
        atr = calculate_atr(data, window=window)
        fig.add_trace(go.Scatter(x=data['date'], y=atr, mode='lines', name=f'ATR ({window})'))
    
    # Update layout for all chart types
    fig.update_layout(
        title={
            'text': f'<b>{company}</b>',
            'x': 0.5,
            'font': {
                'size': 30
            }
        },
        xaxis=dict(
            rangeslider_visible=True,
            rangeselector=dict(
                buttons=rangeselector_buttons,
                bgcolor='lightblue',
                activecolor='darkblue',
                yanchor='top',
                y=-0.4
            ),
            showgrid=True,
            gridcolor=axis_config['gridcolor'],
            gridwidth=axis_config['gridwidth'],
            tickformat=axis_config['tickformat'],
            autorange=True  # Enable dynamic range for x-axis
        ),
        yaxis=dict(
            gridcolor=axis_config['gridcolor'],
            gridwidth=axis_config['gridwidth'],
            tickformat=axis_config['tickformat_y'],
            showgrid=True,
            autorange=True  # Enable dynamic range for y-axis
        ),
        height=chart_height,
        width=chart_width
    )

    return fig


def get_company_info(stock_symbol):
    conn = mysql.connector.connect(
        host="localhost",
        port="3306",
        user="root",
        password="",
        database="infographic_db"
    )
    cursor = conn.cursor(dictionary=True)
    query = 'SELECT * FROM company WHERE stock_symbol = %s'
    cursor.execute(query, (stock_symbol,))
    company_info = cursor.fetchone()
    conn.close()
    return company_info

def analyze_indicator(data, indicator):
    analysis_text = ""
    
    if indicator == "SMA":
        sma = calculate_sma(data, window=20)
        analysis_text = (
            f"Simple Moving Average (SMA): Analyzes trends by smoothing out short-term fluctuations and highlighting longer-term trends. "
            "The SMA is calculated by averaging the closing prices over a specific period, such as 20 days. This helps to filter out daily price "
            "noise and provides a clearer view of the underlying trend. A rising SMA suggests an uptrend, while a declining SMA indicates a downtrend."
        )
        
    elif indicator == "EMA":
        ema = calculate_ema(data, window=20)
        analysis_text = (
            f"Exponential Moving Average (EMA): Provides more weight to recent prices, reacting more quickly to price changes. The EMA is calculated "
            "by applying a weighting factor to the most recent prices, which makes it more responsive to recent market movements compared to the SMA. "
            "This can help traders catch trends earlier and adjust their strategies based on the latest data."
        )
        
    elif indicator == "Bollinger Bands":
        sma, upper_band, lower_band = calculate_bollinger_bands(data, window=20)
        analysis_text = (
            f"Bollinger Bands: Shows volatility and overbought/oversold conditions by plotting bands around a moving average. The bands expand "
            "and contract based on the price volatility. When the price is near the upper band, it may indicate overbought conditions, while a price near "
            "the lower band may signal oversold conditions. This indicator helps in assessing market volatility and potential price reversals."
        )
        
    elif indicator == "Keltner Channels":
        ema_typical_price, upper_channel, lower_channel = calculate_keltner_channels(data, window=20)
        analysis_text = (
            f"Keltner Channels: Displays volatility and trend direction with channels based on an average true range. The channels are centered around "
            "an EMA of the typical price and are adjusted by the average true range to account for market volatility. When the price moves toward the "
            "upper channel, it may indicate a strong uptrend, while movements toward the lower channel may suggest a downtrend."
        )
        
    elif indicator == "Envelopes":
        upper_envelope, lower_envelope = calculate_envelopes(data, window=20)
        analysis_text = (
            f"Envelopes: Helps identify potential buy/sell signals by showing price channels around a moving average. The envelopes are set at fixed "
            "percentages above and below the moving average, creating a range within which the price is expected to fluctuate. When the price breaks out "
            "of the envelope, it may indicate a potential trading opportunity, such as a buy signal when the price is above the upper envelope or a sell signal "
            "when it is below the lower envelope."
        )
        
    elif indicator == "Price Channels":
        high_channel, low_channel = calculate_price_channels(data, window=20)
        analysis_text = (
            f"Price Channels: Shows support and resistance levels by tracking high and low prices over a set period. The channel is formed by plotting the "
            "highest and lowest prices over a defined timeframe. This helps traders identify key price levels where the stock may find support or resistance, "
            "and can be useful for setting entry and exit points based on price movements within the channel."
        )
        
    elif indicator == "Average True Range (ATR)":
        atr = calculate_atr(data, window=20)
        analysis_text = (
            f"Average True Range (ATR): Measures market volatility by calculating the average range of price movements. ATR helps traders understand the "
            "extent of price fluctuations over a set period. A higher ATR value indicates greater volatility and larger price swings, which can be useful for "
            "adjusting stop-loss levels and assessing the risk associated with trades. Conversely, a lower ATR value suggests a more stable market with smaller "
            "price movements."
        )
    
    return analysis_text

def get_indicator_description(indicator):
    descriptions = {
        "SMA": ("The Simple Moving Average (SMA) calculates the average of a stock's price over a specified period. "
                "It helps to smooth out short-term fluctuations and highlight longer-term trends. By averaging out "
                "price data over time, SMA can help investors identify the general direction of the market and make "
                "more informed trading decisions. A longer period SMA reflects a more stable trend, while a shorter "
                "period SMA responds more quickly to price changes."),
                
        "EMA": ("The Exponential Moving Average (EMA) gives more weight to recent prices, making it more responsive "
                "to new information compared to the SMA. This indicator helps traders identify the direction of the trend "
                "more quickly and can signal potential buy or sell opportunities. EMA is often used in combination with other "
                "indicators to confirm trends and avoid false signals. Its responsiveness to recent price movements makes it "
                "popular among short-term traders."),

        "Bollinger Bands": ("Bollinger Bands consist of a middle band, which is an SMA, and two outer bands that are set "
                            "at a certain number of standard deviations from the middle band. This indicator is used to assess "
                            "volatility and identify potential overbought or oversold conditions. When the price moves closer to "
                            "the upper band, it may indicate overbought conditions, while movements towards the lower band may "
                            "suggest oversold conditions. The width of the bands varies with volatility, widening during periods "
                            "of high volatility and narrowing during low volatility."),

        "Keltner Channels": ("Keltner Channels are similar to Bollinger Bands but use the Average True Range (ATR) to set the "
                             "distance between the upper and lower channels. They consist of an upper channel, a lower channel, "
                             "and a middle channel, which is typically an EMA. Keltner Channels help identify trend strength and "
                             "volatility. When the price is consistently hitting the upper channel, it may indicate a strong uptrend, "
                             "while prices approaching the lower channel might signal a downtrend. The channels expand and contract "
                             "with changes in market volatility."),

        "Envelopes": ("Envelopes are bands plotted above and below a moving average to help identify overbought and oversold "
                      "conditions. The distance between the bands and the moving average is usually a fixed percentage. When the "
                      "price moves outside of these bands, it may suggest that the stock is overbought or oversold. Envelopes can "
                      "also help traders to identify potential reversal points. They are simple yet effective for trend-following "
                      "strategies and for setting entry and exit points."),

        "Price Channels": ("Price Channels plot the highest and lowest prices over a specific period, forming an upper and lower "
                            "boundary. This indicator helps traders identify potential support and resistance levels by showing "
                            "where the price tends to bounce off. A breakout above the upper channel may indicate a strong uptrend, "
                            "while a drop below the lower channel might signal a downtrend. Price Channels are useful for setting stop-loss "
                            "orders and for recognizing significant price movements."),

        "Average True Range (ATR)": ("The ATR measures market volatility by calculating the average range of price movements over a "
                                      "set period. It is used to understand market conditions and adjust trading strategies accordingly. "
                                      "A high ATR value indicates increased volatility and larger price swings, while a low ATR value "
                                      "suggests lower volatility and smaller price movements. ATR is often used to set stop-loss levels "
                                      "and to gauge the potential risk and reward of trades.")
    }
    return descriptions.get(indicator, "No description available for this indicator.")

def generate_report(data, chart_type, indicator):
    # Create a BytesIO buffer to hold the PDF data
    buffer = BytesIO()

    # Create a PDF document
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []

    # Create a styles object for better formatting
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['BodyText']
    
    # Fetch company info
    company_info = get_company_info(data['stock_symbol'].iloc[0])
    # Add a title
    story.append(Paragraph("Stock Report", title_style))
    story.append(Spacer(1, 12))
        
    # and company information
    if company_info:
        story.append(Paragraph(f"Company: <b>{company_info['company_name']}</b>", heading_style))
        story.append(Paragraph(f"Description: {company_info['description']}", normal_style))
        story.append(Paragraph(f"Address: {company_info['address']}", normal_style))
        story.append(Paragraph(f"Website: <a href='{company_info['website']}'>{company_info['website']}</a>", normal_style))
        story.append(Spacer(1, 12))
    else:
        story.append(Paragraph("Company information not available.", normal_style))
        story.append(Spacer(1, 12))
        
    # Add chart type
    story.append(Paragraph(f"Chart Type: {chart_type}", heading_style))
    story.append(Spacer(1, 12))
    # Add the chart
    fig = create_chart(data, chart_type, indicator)
    chart_path = "chart.png"
    fig.write_image(chart_path)
    
    # Add chart to PDF
    story.append(Paragraph("Stock Price Chart", heading_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph("See the attached chart below:", normal_style))
    story.append(Spacer(1, 12))
    story.append(Image(chart_path, width=6*inch, height=3*inch))
    story.append(Spacer(1, 12))
    
    # Add Indicator
    story.append(Paragraph(f"Indicator: {indicator if indicator else 'None'}", heading_style))
    story.append(Spacer(1, 12))
    # Add indicator analysis
    analysis_text = analyze_indicator(data, indicator)
    story.append(Paragraph("Indicator Analysis", heading_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(analysis_text, normal_style))
    story.append(Spacer(1, 12))
    # Add indicator description
    indicator_description = get_indicator_description(indicator)
    story.append(Paragraph("Indicator Description", heading_style))
    story.append(Spacer(1, 12))
    story.append(Paragraph(indicator_description, normal_style))
    story.append(Spacer(1, 12))
    # Add chart analysis (You can include details based on your data and chart)
    story.append(Paragraph("Chart Analysis:", heading_style))
    story.append(Paragraph("Placeholder for chart analysis based on your data.", normal_style))

    # Add a note about excluding historical data
    story.append(Spacer(1, 12))
    story.append(Paragraph("Note: Historical data is not included in this report.", normal_style))

    # Build the PDF
    doc.build(story)

    # Return the PDF data
    buffer.seek(0)
    return buffer.getvalue()

    return pdf

# Configure Streamlit and apply custom CSS
configure_streamlit()
apply_custom_css()

# Streamlit layout for controls around the chart
st.sidebar.header("Dashboard Controls")
company = st.sidebar.selectbox("Select Company", df['stock_symbol'].unique(), key='sidebar_company')
st.session_state['company'] = company

def load_css(file_path):
    with open(file_path) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Load the CSS for styling
load_css("styles.css")

# Initialize session state if not already done
if 'page' not in st.session_state:
    st.session_state['page'] = 'main'

# Sidebar buttons for navigating between pages
if st.sidebar.button("Historical Data Visualization", key="historical_data_button"):
    st.session_state['page'] = 'main'
if st.sidebar.button("Real Time Data Visualization", key="real_time_button"):
    st.session_state['page'] = 'real_time'
if st.sidebar.button("Company Comparison Chart", key="comparison_button"):
    st.session_state['page'] = 'comparison'
if st.sidebar.button("Data Overview", key="data_button"):
    st.session_state['page'] = 'data'
if st.sidebar.button("Generate Report", key="report_button"):
    st.session_state['page'] = 'report'

# Navigation logic
if st.session_state.get('page') == 'real_time':
        real_time_visualization_ui()

        

elif st.session_state['page'] == 'data':
    st.title("Data Overview")

    # Define controls for data page
    col1, col2 = st.columns(2)

    with col1:
        selected_company = st.selectbox("Select Company", df['stock_symbol'].unique(), key="data_company")

    with col2:
        selected_year = st.selectbox("Select Year", sorted(df['date'].dt.year.unique()), key="data_year")

    # Filter data based on selection
    data_filtered = df[(df['stock_symbol'] == selected_company) & (df['date'].dt.year == selected_year)]

    # Display filtered data
    st.write(f"Data for {selected_company} in {selected_year}")
    st.dataframe(data_filtered)

elif st.session_state['page'] == 'report':
    st.title("Generate Report")

    # Define controls for report generation
    col1, col2 = st.columns(2)

    with col1:
        chart_type = st.selectbox("Chart Type for Report", ["Bar Chart", "Candlestick Chart", "Line Chart", "Area Chart"])

    with col2:
        indicator = st.selectbox("Indicator for Report", [None, "SMA", "EMA", "Bollinger Bands", "Keltner Channels", "Envelopes", "Average True Range (ATR)", "Price Channels"])

    if st.button("Generate Report"):
        # Generate the PDF report
        report_data = df[df['stock_symbol'] == company]
        pdf_data = generate_report(report_data, chart_type, indicator)
        
        # Provide a download button with the PDF data
        st.download_button(
            label="Download Report",
            data=pdf_data,
            file_name="stock_report.pdf",
            mime="application/pdf"
        )
elif st.session_state['page'] == 'comparison':
    st.title("Comparison Chart")

    # Define columns for selecting the second company, chart type, date range, and indicator selection
    col1, col2, col3 = st.columns(3)

    # Display the first company with similar styling to selectbox
    with col1:
        company1 = st.session_state.get('company', df['stock_symbol'].unique()[0])
        st.selectbox("First Company", [company1], key='select_first_company', disabled=True)

    # Allow user to select the second company with a unique key
    with col2:
        company2 = st.selectbox("Select Second Company", df['stock_symbol'].unique(), key='select_second_company')

    # Only Line Chart is available with a unique key
    with col3:
        chart_type = st.selectbox("Chart", ["Line Chart"], key='chart_type')

    # Define columns for date range and indicator selection
    col4, col5 = st.columns(2)

    # Date range input with a unique key
    with col4:
        date_range = st.date_input("Date Range", [df['date'].min(), df['date'].max()], key='date_range')

    with col5:
        indicator = st.selectbox("Indicator", [None, "SMA", "EMA", "Bollinger Bands", "Keltner Channels", "Envelopes", "Price Channels", "ATR"])

    # Convert date_range to datetime64
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    # Filter the dataframe based on selection
    filtered_df1 = df[(df['stock_symbol'] == company1) & (df['date'] >= start_date) & (df['date'] <= end_date)]
    filtered_df2 = df[(df['stock_symbol'] == company2) & (df['date'] >= start_date) & (df['date'] <= end_date)]

    # Generate comparison chart
    comparison_chart = create_comparison_chart(filtered_df1, filtered_df2, chart_type, indicator)

    # Display the chart using Plotly
    st.plotly_chart(comparison_chart, use_container_width=True)
else:
    st.title("Historical Data Visualization")

    # Define columns for chart type, date range, and indicator selection
    col1, col2, col3 = st.columns(3)

    with col1:
        chart_type = st.selectbox("Chart Type", ["Bar Chart", "Candlestick Chart", "Line Chart", "Area Chart"])

    with col2:
        date_range = st.date_input("Date Range", [df['date'].min(), df['date'].max()])

    with col3:
        indicator = st.selectbox("Indicator", [None, "SMA", "EMA", "Bollinger Bands", "Keltner Channels", "Envelopes", "Average True Range (ATR)", "Price Channels"])

    # Convert date_range to datetime64
    start_date = pd.to_datetime(date_range[0])
    end_date = pd.to_datetime(date_range[1])

    # Filter the dataframe based on selection
    filtered_df = df[(df['stock_symbol'] == company) & (df['date'] >= start_date) & (df['date'] <= end_date)]

    # Generate chart based on selection
    chart = create_chart(filtered_df, chart_type, indicator)

    # Display the chart using Plotly
    st.plotly_chart(chart, use_container_width=True)
    
