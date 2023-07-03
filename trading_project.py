from sqlalchemy import create_engine
import getpass
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Hard-coded settings
user = "root"
password = "65Aiij2woKZHnB3D"
host = "localhost"
database = "trading" # schema

# # Change to this for secure input later
# user = input("Enter username: ")
# password = getpass("Enter password: ")
# host = input("Enter host: ")
# database = input("Enter database: ")

connection_url = f"mysql+mysqlconnector://{user}:{password}@{host}/{database}"
engine = create_engine(connection_url) # create connection

# # example for getting dataframe:
# df = pd.read_sql_table("currencies", con=engine)
# print(df)

def trade_system_menu():
    print("""Main Menu: Trade System Menu
    1) Query
    2) Export trade data"
    3) Reporting
    4) Exit""")

def query_menu():
    print("Query Menu")
    print("1) List brokers")
    print("2) List all share(should include company name)")
    print("3) Lookup trade by trade id(shows all trade details)")
    print("4) Search for trade(specifying one or more of the following: share_id, broker_id, date_range)")
    print("5) Return to main menu")

def trade_data_menu():
    print("Trade Data Menu")
    print("1) Fetch trades by share_id")
    print("2) Fetch trades by broker_id")
    print("3) Fetch trades by date_range")
    print("4) Return to main menu")

def reporting_menu():
    print("Reporting Menu")
    print("1) Number of trades per broker(histogram)")
    print("2) Share price history for a specified share_id(line chart/ connected scatter graph)")
    print("3) Proportion of trades traded on each exchange(pie chart)")
    print("4) Return to main menu")

trade_system_menu()
trade_system_menu_option= int(input("Enter your option: "))
if trade_system_menu_option != 0:
    if trade_system_menu_option == 1:
        query_menu()
        query_menu_option= int(input("Enter your option:"))
        while query_menu_option != 0:
            if query_menu_option == 1:
                print("List of brokers \n")
                brokers= pd.read_sql_table("brokers", con=engine)
                print(brokers)
            elif query_menu_option ==2:
                print("List of shares")
                shares= pd.read_sql('SELECT shares.share_id, companies.name AS company_name FROM companies INNER JOIN shares ON companies.company_id = shares.company_id ORDER BY shares.share_id ', con=engine)
                print(shares)
            elif query_menu_option ==3:
                trade_id_query= int(input("Enter the trade ID: "))
                print("Trade information: ")
                trade_info= pd.read_sql(f"SELECT * FROM trades WHERE trade_id='{trade_id_query}'", con=engine)
                print(trade_info) 
            elif query_menu_option == 4:
                share_id_search= int(input("Enter the share ID (0 to ignore): "))
                broker_id_search= int(input("Enter the broker ID (0 to ignore): "))
                start_date_search= input("Enter the start date (YYYY-MM-DD)(leave to ignore): ")
                end_date_search= input("Enter the end date (YYYY-MM-DD)(leave to ignore): ")

                where_clause= ""
                if share_id_search != 0:
                    where_clause += f"share_id={share_id_search}"
                if broker_id_search != 0:
                    if where_clause: 
                        where_clause += " AND "
                    where_clause += f"broker_id={broker_id_search}"
                if start_date_search and end_date_search:
                    if where_clause: 
                        where_clause += " AND "
                    where_clause += f"transaction_time BETWEEN '{start_date_search}' AND '{end_date_search}'"
                
                query= f"SELECT * FROM trades"
                if where_clause:
                    query += f" WHERE {where_clause}"
                trade_info= pd.read_sql(query, con=engine)
                print("Trades: ")
                print(trade_info)
                
            elif query_menu_option ==5:
                trade_system_menu()
                trade_system_menu_option= int(input("Enter your option: "))

            else: 
                print("Invalid option")
                exit()
            query_menu()
            query_menu_option= int(input("Enter your option:"))

    elif trade_system_menu_option == 2:
        trade_data_menu()
        trade_data_menu_option= int(input("Enter your option: "))
        while trade_data_menu_option != 0:
            if trade_data_menu_option == 1:
                share_id_search= int(input("Enter share id: "))
                trade_share_id= pd.read_sql(f"SELECT * FROM trades WHERE share_id='{share_id_search}'", con=engine)
                print(trade_share_id)
            elif trade_data_menu_option == 2:
                broker_id_search= int(input("Enter broker id: "))
                broker_share_id= pd.read_sql(f"SELECT * FROM trades WHERE broker_id='{broker_id_search}'", con=engine)
                print(broker_share_id)
            elif trade_data_menu_option == 3:
                start_date_search= input("Enter the start date (YYYY-MM-DD): ")
                end_date_search= input("Enter the end date (YYYY-MM-DD): ")
                date_range_share_id= pd.read_sql(f"SELECT * FROM trades WHERE transaction_time BETWEEN '{start_date_search}' AND '{end_date_search}'", con=engine)
                print(date_range_share_id)
            elif trade_data_menu_option == 4:
                trade_system_menu()
                trade_system_menu_option= int(input("Enter your option: "))
            else: 
                print("Invalid option")
                exit()
            trade_data_menu()
            trade_data_menu_option= int(input("Enter your option: "))

    elif trade_system_menu_option == 3:
        reporting_menu()
        reporting_menu_option= int(input("Enter your option: "))
        while reporting_menu_option != 0:
            if reporting_menu_option == 1:
                broker_trade_counts= pd.read_sql("SELECT broker_id, COUNT(*) as trade_count FROM trades GROUP BY broker_id", con=engine)
                plt.bar(broker_trade_counts['broker_id'], broker_trade_counts['trade_count'])
                plt.xlabel('Broker ID')
                plt.ylabel('Number of trades')
                plt.title('Number of trades per broker')
                plt.show()
            elif reporting_menu_option == 2:
                chosen_share_id= int(input("Enter share ID: "))
                price_history= pd.read_sql(f"SELECT time_start, price FROM shares_prices WHERE share_id='{chosen_share_id}'", con=engine)
                #convert transaction_time to datetime if needed
                price_history['time_start']=pd.to_datetime(price_history['time_start'])
                #sort dataframe by transaction_time
                price_history= price_history.sort_values('time_start')
                plt.plot(price_history['time_start'], price_history['price'])
                plt.xlabel('Transaction Time')
                plt.ylabel('Share Price')
                plt.title(f'Price History for Share ID {chosen_share_id}')
                plt.show()
            elif reporting_menu_option == 3:
                exchange_trade_counts= pd.read_sql("SELECT stock_exchanges.name as stock_exchange_name, COUNT(*) as trade_count FROM trades RIGHT OUTER JOIN stock_exchanges ON trades.stock_ex_id=stock_exchanges.stock_ex_id GROUP BY stock_exchanges.stock_ex_id", con=engine)
                plt.pie(exchange_trade_counts['trade_count'], labels=exchange_trade_counts['stock_exchange_name'], autopct='%1.1f%%')
                plt.title('Proportion of Trades per Stock Exchange')
                plt.show()
            elif reporting_menu_option == 4:
                trade_system_menu()
                trade_system_menu_option= int(input("Enter your option: "))
            else: 
                print("Invalid option")
                exit()
            reporting_menu()
            reporting_menu_option= int(input("Enter your option: "))

    elif trade_system_menu_option == 4:
        print("Goodbye.")
        exit()
    else:
        print("Invalid option. Try again.")
        trade_system_menu()
        trade_system_menu_option= int(input("Enter your option: "))
else: 
    print("Invalid option. Try again.")
    trade_system_menu()
    trade_system_menu_option= int(input("Enter your option: "))
engine.dispose() # dispose the connection
