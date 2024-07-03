import mysql.connector
import configparser

# Configuration file path
CONFIG_PATH = 'config.ini'


# def get_database_connection():
#     # Read the configuration file
#     config = configparser.ConfigParser()
#     config.read(CONFIG_PATH)

#     # Get the MySQL database configuration
#     db_config = {
#         'host': config['mysql']['host'],
#         'user': config['mysql']['user'],
#         'password': config['mysql']['password'],
#         'database': config['mysql']['database']
#     }

#     # Establish a connection to the MySQL database
#     connection = mysql.connector.connect(
#         host=db_config['host'],
#         user=db_config['user'],
#         password=db_config['password'],
#         database=db_config['database']
#     )
#     return connection
def get_database_connection():
    # Read the configuration file
    config = configparser.ConfigParser()
    config.read(CONFIG_PATH)

    # Get the MySQL database configuration
    db_config = {
        'host': config['mysql']['host'],
        'user': config['mysql']['user'],
        'password': config['mysql']['password'],
    }

    # Establish a connection to the MySQL server (no database specified)
    connection = mysql.connector.connect(**db_config)
    return connection


connection = get_database_connection()
def execute_query( query):
    cursor = connection.cursor()
    res=cursor.execute(query)
    #print(res)
    connection.commit()
    cursor.close()

def get_all_tables(cursor,old_database_name):
    cursor.execute(f"SELECT table_name FROM {old_database_name}.meta_load_status where load_status='0'")
    tables = cursor.fetchall()
    # print(tables)
    # print(f"SELECT table_name FROM {old_database_name}.meta_load_status where load_status='0'")
    return [table[0] for table in tables]

# def add_columns(cursor, table_name):
#     alter_table_query = f"""
#     ALTER TABLE {table_name}
#     ADD COLUMN  Daily_Return FLOAT,
#     ADD COLUMN  MA_5_Day FLOAT,
#     ADD COLUMN  MA_10_Day FLOAT,
#     ADD COLUMN  Volatility FLOAT,
#     ADD COLUMN  RSI FLOAT,
#     ADD COLUMN  MACD FLOAT,
#     ADD COLUMN  Signal1 FLOAT,
#     ADD COLUMN  Upper_Band FLOAT,
#     ADD COLUMN  Lower_Band FLOAT;
#     ADD COLUMN  Gain FLOAT,
#     ADD COLUMN  Loss FLOAT,
#     ADD COLUMN  AvgGain FLOAT,
#     ADD COLUMN  AvgLoss FLOAT
#     """
#     #print(alter_table_query)
#     cursor.execute(alter_table_query)

# def column_exists(cursor, table_name, column_name):
#     cursor.execute(f"SHOW COLUMNS FROM {table_name} LIKE '{column_name}'")
#     return cursor.fetchone() is not None

# def add_column_if_not_exists(cursor, table_name, column_name, column_type):
#     if not column_exists(cursor, table_name, column_name):
#         execute_query(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")

# def add_columns(cursor, table_name):
#     columns = {
#         "Daily_Return": "FLOAT",
#         "MA_5_Day": "FLOAT",
#         "MA_10_Day": "FLOAT",
#         "Volatility": "FLOAT",
#         "RSI": "FLOAT",
#         "MACD": "FLOAT",
#         "Signal1": "FLOAT",
#         "Upper_Band": "FLOAT",
#         "Lower_Band": "FLOAT",
#         "Gain": "FLOAT",
#         "Loss": "FLOAT",
#         "AvgGain": "FLOAT",
#         "AvgLoss": "FLOAT",
#         "EMA_12":"FLOAT",
#         "EMA_26":"FLOAT",
#         "MA_20":"FLOAT",
#         "SD_20":"FLOAT"

#     }
    
#     for column_name, column_type in columns.items():
#         add_column_if_not_exists(cursor, table_name, column_name, column_type)
def create_new_database(cursor, new_database_name):
    create_database_query = f"CREATE DATABASE IF NOT EXISTS {new_database_name};"
    cursor.execute(create_database_query)

def create_new_table(cursor, new_database_name, new_table_name):
    cursor.execute(f"drop table IF EXISTS  {new_database_name}.{new_table_name}")

    create_table_query = f"""
    CREATE TABLE {new_database_name}.{new_table_name} (
        Date DATE,
        Open FLOAT,
        High FLOAT,
        Low FLOAT,
        Close FLOAT,
        Volume INT,
        OpenInt INT,
        Daily_Return FLOAT,
        MA_5_Day FLOAT,
        MA_10_Day FLOAT,
        Volatility FLOAT,
        RSI FLOAT,
        MACD FLOAT,
        Signal_9 FLOAT,
        Upper_Band FLOAT,
        Lower_Band FLOAT,
        Gain FLOAT,
        Loss FLOAT,
        AvgGain FLOAT,
        AvgLoss FLOAT,
        EMA_12 FLOAT,
        EMA_26 FLOAT,
        MA_20 FLOAT,
        SD_20 FLOAT,
        PRIMARY KEY (Date)
    );
    """
    #print(create_table_query)
    execute_query(create_table_query)
    import time
    # time.sleep(5)

def insert_data_from_existing(cursor,old_database_name, source_table, new_database_name, new_table):
    insert_query = f"""
    INSERT INTO {new_database_name}.{new_table}
    SELECT distinct Date, Open, High, Low, Close, Volume, OpenInt, 
           null Daily_Return,  null MA_5_Day,null MA_10_Day,null Volatility,null RSI,
           null MACD,null Signal1,null Upper_Band,null Lower_Band,null Gain,null Loss,null AvgGain,null AvgLoss,null EMA_12,null EMA_26,null MA_20,null SD_20
    FROM {old_database_name}.{source_table};
    """
    #print(insert_query)
    execute_query(insert_query)

def calculate_daily_return(cursor,new_database_name, table_name):
    update_query = f"""
    UPDATE {new_database_name}.{table_name}
    SET Daily_Return = (Close - Open) / Open
    where Open!=0;
    """
    #print(update_query)
    execute_query(update_query)

def calculate_moving_averages(cursor,new_database_name, table_name):
    update_query_5_day = f"""
    UPDATE {new_database_name}.{table_name} t1
    JOIN (
        SELECT Date, 
               AVG(Close) OVER (ORDER BY Date ROWS BETWEEN 4 PRECEDING AND CURRENT ROW) AS MA_5_Day
        FROM {new_database_name}.{table_name}
    ) t2 ON t1.Date = t2.Date
    SET t1.MA_5_Day = t2.MA_5_Day;
    """
    #print(update_query_5_day)
    execute_query(update_query_5_day)

    update_query_10_day = f"""
    UPDATE {new_database_name}.{table_name} t1
    JOIN (
        SELECT Date, 
               AVG(Close) OVER (ORDER BY Date ROWS BETWEEN 9 PRECEDING AND CURRENT ROW) AS MA_10_Day
        FROM {new_database_name}.{table_name}
    ) t2 ON t1.Date = t2.Date
    SET t1.MA_10_Day = t2.MA_10_Day;
    """
    #print(update_query_10_day)

    execute_query(update_query_10_day)

def calculate_volatility(cursor, new_database_name,table_name):
    update_query = f"""
    UPDATE {new_database_name}.{table_name}
    SET Volatility = (High - Low) / Open
    where Open!=0;
    """
    execute_query(update_query)

def calculate_rsi(cursor, new_database_name,table_name):
    # RSI calculation typically involves multiple steps; here's a simplified version
    gain_loss_query = f"""
        UPDATE  {new_database_name}.{table_name} t1
    JOIN (
        SELECT Date,
               IF(@prev_close IS NULL, NULL, GREATEST(0, Close - @prev_close)) AS Gain,
               IF(@prev_close IS NULL, NULL, GREATEST(0, @prev_close - Close)) AS Loss,
               @prev_close := Close
        FROM  {new_database_name}.{table_name}
        ORDER BY Date
    ) t2 ON t1.Date = t2.Date
    SET t1.Gain = t2.Gain, t1.Loss = t2.Loss;

    """
    #print(gain_loss_query)
    execute_query(gain_loss_query)

    avg_gain_loss_query = f"""
    UPDATE {new_database_name}.{table_name} t1
    JOIN (
        SELECT Date,
               AVG(Gain) OVER (ORDER BY Date ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) AS AvgGain,
               AVG(Loss) OVER (ORDER BY Date ROWS BETWEEN 13 PRECEDING AND CURRENT ROW) AS AvgLoss
        FROM {new_database_name}.{table_name}
    ) t2 ON t1.Date = t2.Date
    SET t1.AvgGain = t2.AvgGain, t1.AvgLoss = t2.AvgLoss;
    """
    #print(avg_gain_loss_query)
    execute_query(avg_gain_loss_query)

    rsi_query = f"""
    UPDATE {new_database_name}.{table_name}
    SET RSI = 100 - (100 / (1 + (AvgGain / AvgLoss)))
    where AvgLoss!=0 ;
    """
    #print(rsi_query)
    execute_query(rsi_query)

def calculate_macd(cursor,new_database_name,old_database_name, table_name):
    # MACD and Signal calculations typically involve multiple steps
    ema_12_query = f"""
CALL {old_database_name}.CalculateEMA12("{new_database_name}.{table_name}");
    """
    #print(ema_12_query)
    execute_query(ema_12_query)

    ema_26_query = f"""
    CALL {old_database_name}.CalculateEMA26("{new_database_name}.{table_name}");

    """
    #print(ema_26_query)
    execute_query(ema_26_query)

    macd_query = f"""
    UPDATE {new_database_name}.{table_name}
    SET MACD = EMA_12 - EMA_26;
    """
    #print(macd_query)
    execute_query(macd_query)

    signal_query = f"""
CALL {old_database_name}.CalculateSignal9('{new_database_name}.{table_name}');

    """
    execute_query(signal_query)

def calculate_bollinger_bands(cursor,new_database_name, table_name):
    moving_averages_query = f"""
    UPDATE {new_database_name}.{table_name} t1
    JOIN (
        SELECT Date,
               AVG(Close) OVER (ORDER BY Date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS MA_20,
               STDDEV(Close) OVER (ORDER BY Date ROWS BETWEEN 19 PRECEDING AND CURRENT ROW) AS SD_20
        FROM {new_database_name}.{table_name}
    ) t2 ON t1.Date = t2.Date
    SET t1.MA_20 = t2.MA_20, t1.SD_20 = t2.SD_20;
    """
    execute_query(moving_averages_query)

    upper_band_query = f"""
    UPDATE {new_database_name}.{table_name}
    SET Upper_Band = MA_20 + 2 * SD_20;
    """
    execute_query(upper_band_query)

    lower_band_query = f"""
    UPDATE {new_database_name}.{table_name}
    SET Lower_Band = MA_20 - 2 * SD_20;
    """
    #print(lower_band_query)
    execute_query(lower_band_query)
def disable_safe_update_mode(connection):
    query = "SET SQL_SAFE_UPDATES = 0;"
    execute_query( query)
def update_status(cursor,old_database_name, table_name):
    update_query = f"""
        UPDATE {old_database_name}.meta_load_status as t1
    JOIN (
        SELECT table_name,
               '1' as load_status,
               CURRENT_TIMESTAMP as last_updated
        FROM {old_database_name}.meta_load_status where table_name='{table_name}'
    ) t2 ON t1.table_name = t2.table_name 
    SET t1.load_status = t2.load_status, t1.last_updated = t2.last_updated;
    """
    execute_query(update_query)
def main():
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        disable_safe_update_mode(connection)
        old_database_name="raw_layer"
        tables = get_all_tables(cursor,old_database_name)
        # tables=['raw_aadr_us']
        new_database_name="int_layer"
        create_new_database(cursor, new_database_name)
        for table in tables:
            new_table=f"int_{table}"
            print(f"Modifying table: {new_table}")
            create_new_table(cursor, new_database_name, new_table)
            # print("fhgdcj")
            insert_data_from_existing(cursor, old_database_name,table, new_database_name, new_table)
            calculate_daily_return(cursor, new_database_name,new_table)
            calculate_moving_averages(cursor, new_database_name,new_table)
            calculate_volatility(cursor, new_database_name,new_table)
            calculate_rsi(cursor, new_database_name,new_table)
            calculate_macd(cursor, new_database_name,old_database_name,new_table)
            calculate_bollinger_bands(cursor, new_database_name,new_table)
            update_status(cursor, old_database_name,table)
            # connection.commit()

        print("All tables modified successfully.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

if __name__ == "__main__":
    main()
