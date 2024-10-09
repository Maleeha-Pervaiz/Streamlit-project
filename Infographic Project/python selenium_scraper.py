import pymysql
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time  # Import the time module
import threading

companies = ["ogdc", "ppl", "kel"]

# Define a function to search and extract data
def search_and_extract_data(company_name, data_list):
    try:
        # Find the search input element and enter the company name
        search_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="DataTables_Table_0_filter"]/label/input'))
        )
        search_input.clear()
        search_input.send_keys(company_name)
        search_input.send_keys(Keys.RETURN)
        
        # Wait for the table to be updated with search results
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="DataTables_Table_0"]'))
        )
        
        # Extract data from the table
        rows = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="DataTables_Table_0"]/tbody/tr'))
        )
        
        # Get the current timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        for row in rows:
            cells = row.find_elements(By.XPATH, './/td')
            data = [cell.text for cell in cells]
            # Ensure the first cell contains the exact company name
            if data[0].strip().lower() == company_name.lower():
                # Extract only the specified columns (adjust indices if needed)
                filtered_data = [data[i] for i in [2, 3, 4, 5, 8]] 
                volume = cells[8].text.strip().replace(',', '')
                # Prepend the timestamp to the filtered data
                full_data = [timestamp] + filtered_data
                data_list.append({'Timestamp': timestamp, 'Symbol': company_name, 'Open': filtered_data[0], 'High': filtered_data[1], 'Low': filtered_data[2], 'Current': filtered_data[3], 'Volume': volume })
                print(f"Data for {company_name}: {full_data}")
    
    except Exception as e:
        print(f"Error: {e}")

def connect_to_mysql():
    try:
        connection = pymysql.connect(host='localhost',
                                     user='root',
                                     password='',
                                     database='infographic_db')
        print("Connection to MySQL established successfully.")
        return connection
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL: {e}")
        return None
    
# Function to insert data into MySQL
def insert_data(connection, data_dict):
    if connection is None:
        print("No connection to MySQL. Exiting insert_data function.")
        return
    cursor = connection.cursor()
    try:
        sql = "INSERT INTO real_time_data (timestamp, stock_symbol, open_price, high_price, low_price, current_price, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        values = (data_dict['Timestamp'], data_dict['Symbol'], data_dict['Open'], data_dict['High'], data_dict['Low'], data_dict['Current'], data_dict['Volume'])
        cursor.execute(sql, values)
        print(f"Inserted data into database.")
    except pymysql.MySQLError as e:
        print(f"Error inserting data: {e}")
    connection.commit()
    cursor.close()



# Infinite loop to run the program continuously
while True:
    driver = webdriver.Chrome()
    driver.get("https://dps.psx.com.pk/")
    # Collect data
    data_list = []
    for company in companies:
        search_and_extract_data(company, data_list)

    # Connect to MySQL
    connection = connect_to_mysql()

    if connection:
        # Insert data into MySQL
        for data in data_list:
            insert_data(connection, data)

        # Close the connection
        connection.close()
    driver.quit()

    # Pause for 5 minutes (300 seconds) before the next iteration
    time.sleep(86400)

# Start the data fetching process in a separate thread
threading.Thread(target=continuous_data_fetch).start()