""" 
Description: 
  Divides sales data CSV file into individual order data Excel files.

Usage:
  python process_sales_data.py sales_csv_path

Parameters:
  sales_csv_path = Full path of the sales data CSV file
"""
import pandas as pd
import sys
import os.path
from datetime import date
import re

def main():
    sales_csv_path = get_sales_csv_path()
    orders_dir_path = create_orders_dir(sales_csv_path)
    process_sales_data(sales_csv_path, orders_dir_path)

def get_sales_csv_path():
    """Gets the path of sales data CSV file from the command line

    Returns:
        str: Path of sales data CSV file
    """
    # TODO: Check whether command line parameter provided
    num_params = len(sys.argv) - 1
    if num_params < 1:
        print("Error: Missing CSV path parameter.")
        sys.exit()

    # TODO: Check whether provide parameter is valid path of file
    csv_path = sys.argv[1]
    if not os.path.isfile(csv_path):
        print("Error: CSV path is not an existing file.")
        sys.exit()

    # TODO: Return path of sales data CSV file
    return os.path.abspath(csv_path) 
    

def create_orders_dir(sales_csv_path):
    """Creates the directory to hold the individual order Excel sheets

    Args:
        sales_csv_path (str): Path of sales data CSV file

    Returns:
        str: Path of orders directory
    """
    # TODO: Get directory in which sales data CSV file resides
    sales_csv_dir = os.path.dirname(sales_csv_path)
    
        
    # TODO: Determine the path of the directory to hold the order data files
    todays_date = date.today().isoformat()
    orders_dir = f'orders_{todays_date}'
    orders_dir_path = os.path.join(sales_csv_dir, orders_dir)

    # TODO: Create the orders directory if it does not already exist
    if not os.path.isdir(orders_dir_path):
        os.makedirs(orders_dir_path)

    # TODO: Return path of orders directory
    return orders_dir_path

def process_sales_data(sales_csv_path, orders_dir_path):
    """Splits the sales data into individual orders and save to Excel sheets

    Args:
        sales_csv_path (str): Path of sales data CSV file
        orders_dir_path (str): Path of orders directory
    """
    # Import the sales data from the CSV file into a DataFrame
    df = pd.read_csv(sales_csv_path)


    # TODO: Insert a new "TOTAL PRICE" column into the DataFrame
    df.insert(7, 'TOTAL PRICE', df['ITEM QUANTITY'] * df['ITEM PRICE'])


    # TODO: Remove columns from the DataFrame that are not needed
    df.drop(columns=['ADDRESS','CITY','STATE','POSTAL CODE', 'COUNTRY'], inplace=True)


    # TODO: Groups orders by ID and iterate 
    
    for order_id, order_df in df.groupby('ORDER ID'): 

        # TODO: Remove the 'ORDER ID' column
        order_df.drop(columns=['ORDER ID'], inplace=True)

        # TODO: Sort the items by item number
        order_df.sort_values(by='ITEM NUMBER', inplace=True)

        # TODO: Append a "GRAND TOTAL" row
        grand_total = order_df['TOTAL PRICE'].sum()
        grand_total_df = pd.DataFrame({'ITEM PRICE': ['GRAND TOTAL'], 'TOTAL PRICE': [grand_total]})
        order_df = pd.concat([order_df, grand_total_df])
        

        # TODO: Determine the file name and full path of the Excel sheet
        customer_name = order_df['CUSTOMER NAME'].values[0]
        customer_name = re.sub(r'\W', '', customer_name)
        
        

        # TODO: Export the data to an Excel sheet
       
       

        # TODO: Format the Excel sheet
        writer = pd.ExcelWriter("pandas_column_formats.xlsx", engine='xlsxwriter')
        df.to_excel(writer, sheet_name="Sheet1")
        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]


        # TODO: Define format for the money columns
        format1 = workbook.add_format({'num_format': "#,##0.00"})
        format2 = workbook.add_format({'num_format': "0%"})

        # TODO: Format each colunm
        worksheet.set_column(1, 1, 18, format1)
        worksheet.set_column(2, 2, None, format2)


        # TODO: Close the Excelwriter 
        writer.close()
    return



if __name__ == '__main__':
    main()