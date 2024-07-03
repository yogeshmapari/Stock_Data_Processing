import mysql.connector
import configparser
import shutil
import os

def load_data_to_mysql(file_path, config_path, table_name,archive_folder):
    try:
        # Read the configuration file
        config = configparser.ConfigParser()
        config.read(config_path)

        # Get the MySQL database configuration
        db_config = {
            'host': config['mysql']['host'],
            'user': config['mysql']['user'],
            'password': config['mysql']['password'],
            'database': config['mysql']['database']
        }

        # Establish a connection to the MySQL database
        connection = mysql.connector.connect(
            host=db_config['host'],
            user=db_config['user'],
            password=db_config['password'],
            database=db_config['database']
        )
        cursor = connection.cursor()

        # Create the table if it doesn't exist
        create_table_query = f"""
        CREATE TABLE  IF NOT EXISTS   {table_name} (
            Date DATE,
            Open FLOAT,
            High FLOAT,
            Low FLOAT,
            Close FLOAT,
            Volume INT,
            OpenInt INT
        );
        """
        cursor.execute(create_table_query)
        connection.commit()

        # Read the data from the text file
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # Skip the header line
        lines = lines[1:]

        # Insert the data into the table
        for line in lines:
            fields = line.strip().split(',')
            insert_query = f"INSERT INTO {table_name} (Date, Open, High, Low, Close, Volume, OpenInt) VALUES (%s, %s, %s, %s, %s, %s, %s)"
            cursor.execute(insert_query, tuple(fields))
        

        print("Data loaded successfully.")
        # Move the processed file to the archive folder
        shutil.move(file_path, os.path.join(archive_folder, os.path.basename(file_path)))
        print(f"Moved {file_path} to {archive_folder}.")
        
        insert_query1=f"INSERT INTO raw_layer.meta_load_status (table_name, load_status,last_updated)  VALUES ('{table_name}', '0',null)"
        print(insert_query1)
        cursor.execute(insert_query1)
        connection.commit()
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
            print("MySQL connection is closed.")

# # Path to the text file
# file_path = 'stock_market\\aadr.us.txt'
# archive_folder = 'stock_market\\archive_area'
# # Path to the configuration file
# config_path = 'stock_market\config.ini'

# # Name of the table
# table_name = 'raw_aadr_us'

# # Load data into MySQL
# load_data_to_mysql(file_path, config_path, table_name)

if __name__ == "__main__":
    import sys
    # if len(sys.argv) != 5:
    #     print("Usage: python load_data.py <file_path> <config_path> <table_name> <archive_folder>")
    #     sys.exit(1)

    file_path = sys.argv[1]
    config_path = 'config.ini'
    table_name="raw_s_"+"_".join(file_path.split('\\')[-1].split('.')[0:2])
    print(table_name)
    # table_name = sys.argv[3]
    archive_folder = 'archive_area'

    load_data_to_mysql(file_path, config_path, table_name, archive_folder)