import pymysql
import pymysql.cursors
import os
import openai
import json


db_name = None
db_user = None
db_password = None
db_host = None
db_port = 3306


# This function accepts mySQL db credentials and an sql query and executes it 
def get_mysql_db_connection(db_user, db_password, db_host, db_port, db_name):
    """
    Establishes and returns a connection to the MySQL database.

    The database credentials are hardcoded in this function. In a real-world scenario,
    it's better to use environment variables or a configuration file to handle credentials securely.

    :return: A pymysql connection object
    """
    db_credentials = {
        'host': db_host,
        'user': db_user,
        'password': db_password,
        'database': db_name,
        'port': db_port,  # Update with your db port
        'cursorclass': pymysql.cursors.DictCursor
    }
    
    try:
        connection = pymysql.connect(**db_credentials)
        return connection
    except Exception as e:
        print(f"Failed to connect to the database: {e}")
        return None


def get_mysql_database_schema():
    """
    Retrieves the schema (tables and columns with types) of the specified database using a connection established by get_db_connection.
    """
    schema_info = {}
    try:
        connection = get_mysql_db_connection(db_user, db_password, db_host, db_port, db_name) # pass these as global variables
        if connection is None:
            return None

        with connection.cursor() as cursor:
            # Fetching all table names in the database
            tables_query = "SHOW TABLES"
            cursor.execute(tables_query)
            tables = cursor.fetchall()

            for table in tables:
                # The key for table names in the result might vary, so adjust as needed
                table_name = list(table.values())[0]
                schema_info[table_name] = []

                # Fetching all column names and types for a table
                columns_query = f"SHOW COLUMNS FROM {table_name}"
                cursor.execute(columns_query)
                columns = cursor.fetchall()

                for column in columns:
                    column_info = {
                        "name": column["Field"],
                        "type": column["Type"]
                    }
                    schema_info[table_name].append(column_info)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

    return schema_info




def set_database_config(name, user, password, host, port):
    """
    Updates the global database configuration variables.
    
    Args:
    - name: The name of the database.
    - user: The username for the database.
    - password: The password for the database.
    - host: The host of the database.
    - port: The port number for the database connection.
    
    Raises:
    - ValueError: If any of the arguments is None or if port is not an integer.
    """
    global db_name, db_user, db_password, db_host, db_port
    
    # Check for None values and port being an integer
    if None in (name, user, password, host) or not isinstance(port, int):
        raise ValueError("All parameters must be provided and 'port' must be an integer.")
    
    # Update global variables
    db_name = name
    db_user = user
    db_password = password
    db_host = host
    db_port = port

def check_db_config_variables():
    """
    Checks the global database configuration variables for None, null, or empty values.
    
    Returns:
    - A list of variable names that are None, null, or empty.
    """
    # List of variable names and their values
    variables = {
        'db_name': db_name,
        'db_user': db_user,
        'db_password': db_password,
        'db_host': db_host,
        'db_port': db_port
    }
    
    # Check for None, null, or empty values
    invalid_vars = [name for name, value in variables.items() if value is None or value == '']
    if invalid_vars:
        print("The following configuration variables are invalid:", ', '.join(invalid_vars))
    else:
        print("All configuration variables are set correctly.")
    
    return invalid_vars

def get_db_connection(engine, db_user, db_password, db_host, db_port, db_name):
    """
    Attempts to establish a database connection based on the specified SQL engine and returns a message indicating
    the connection status or the encountered error.
    
    :param engine: SQL engine (MySQL, PostgreSQL, or MsSQL)
    :param db_user: Database username
    :param db_password: Database password
    :param db_host: Database host
    :param db_port: Database port
    :param db_name: Database name
    :return: A string message indicating the connection status or error encountered.
    """
    try:
        if engine == "MySQL":
            import pymysql
            pymysql.connect(
                host=db_host,
                user=db_user,
                password=db_password,
                database=db_name,
                port=db_port
            )
        elif engine == "PostgreSQL":
            import psycopg2
            psycopg2.connect(
                user=db_user,
                password=db_password,
                host=db_host,
                port=db_port,
                database=db_name
            )
        elif engine == "MsSQL":
            import pyodbc
            connection_str = f"DRIVER={{SQL Server}};SERVER={db_host},{db_port};DATABASE={db_name};UID={db_user};PWD={db_password}"
            pyodbc.connect(connection_str)
        else:
            return "Unsupported SQL engine specified."

        return "Success! Connection Established! ."

    except Exception as e:
        return f"Failed to connect to {engine} database: {e}"


#db_info = get_database_schema()
#print(db_info)

def execute_mysql_query(sql_query):
    """
    Executes the given SQL query using the database connection established by get_db_connection.

    :param sql_query: SQL query to be executed
    :return: Query results or None if an error occurs
    """
    try:
        connection = get_mysql_db_connection(db_user, db_password, db_host, db_port, db_name) # pass these as global variables
        if connection is None:
            return None

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            results = cursor.fetchall()
            return results
    except Exception as e:
        print(f"An error occurred while executing the query: {e}")
        return None
    finally:
        if connection:
            connection.close()


# POSTGRES DB 
            
import psycopg2
from psycopg2 import OperationalError
import psycopg2.extras


def get_pgdb_connection(db_user, db_password, db_host, db_port, db_name):
    try:
        connection = psycopg2.connect(
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
            database=db_name
        )
        return connection
    except OperationalError as e:
        print(f"The error '{e}' occurred")
        return None


def execute_pgdb_query(sql_query):
    """
    Executes the given SQL query using the database connection established by get_db_connection.
    
    :param sql_query: SQL query to be executed
    :return: Query results or None if an error occurs
    """
    connection = None
    try:
        connection = get_pgdb_connection(db_user, db_password, db_host, db_port, db_name)
        if connection is None:
            return None

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            # For SELECT queries
            if sql_query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
            else:
                # For INSERT/UPDATE/DELETE etc., commit and don't fetch results
                connection.commit()
                results = None
            return results
    except Exception as e:
        print(f"An error occurred while executing the query: {e}")
        return None
    finally:
        if connection:
            connection.close()


def get_pgdb_schema():
    """
    Retrieves the schema (tables and columns with types) of the specified PostgreSQL database using a connection
    established by get_db_connection.
    """
    schema_info = {}
    try:
        connection = get_pgdb_connection(db_user, db_password, db_host, db_port, db_name)
        if connection is None:
            return None

        with connection.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            # Fetching all table names in the database
            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
            """)
            tables = cursor.fetchall()

            for table in tables:
                table_name = table['table_name']
                schema_info[table_name] = []

                # Fetching all column names and types for a table
                cursor.execute(f"""
                    SELECT column_name, data_type
                    FROM information_schema.columns
                    WHERE table_name = %s
                """, (table_name,))
                columns = cursor.fetchall()

                for column in columns:
                    column_info = {
                        "name": column["column_name"],
                        "type": column["data_type"]
                    }
                    schema_info[table_name].append(column_info)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'connection' in locals() and connection:
            connection.close()

    return schema_info


#MsSQL server 

import pyodbc

def get_mssql_db_connection(db_user, db_password, db_host, db_port, db_name):
    try:
        # Forming the connection string
        connection_str = f"DRIVER={{SQL Server}};SERVER={db_host},{db_port};DATABASE={db_name};UID={db_user};PWD={db_password}"
        connection = pyodbc.connect(connection_str)
        return connection
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
   

def execute_mssql_query(sql_query):
    """
    Executes the given SQL query using the database connection established by get_db_connection.

    :param sql_query: SQL query to be executed
    :return: Query results or None if an error occurs
    """
    connection = None
    try:
        connection = get_mssql_db_connection(db_user, db_password, db_host, db_port, db_name)
        if connection is None:
            return None

        with connection.cursor() as cursor:
            cursor.execute(sql_query)
            # For SELECT queries
            if sql_query.strip().upper().startswith("SELECT"):
                results = cursor.fetchall()
            else:
                # For INSERT/UPDATE/DELETE etc., commit and don't fetch results
                connection.commit()
                results = None
            return results
    except Exception as e:
        print(f"An error occurred while executing the query: {e}")
        return None
    finally:
        if connection:
            connection.close()


def get_mssql_db_schema():
    """
    Retrieves the schema (tables and columns with types) of the specified MS SQL Server database using a connection
    established by get_db_connection.
    """
    schema_info = {}
    try:
        connection = get_mssql_db_connection(db_user, db_password, db_host, db_port, db_name)
        if connection is None:
            return None

        with connection.cursor() as cursor:
            # Fetching all table names in the database
            cursor.execute("""
                SELECT TABLE_NAME
                FROM INFORMATION_SCHEMA.TABLES
                WHERE TABLE_TYPE = 'BASE TABLE'
            """)
            tables = cursor.fetchall()

            for table in tables:
                table_name = table.TABLE_NAME
                schema_info[table_name] = []

                # Fetching all column names and types for a table
                cursor.execute(f"""
                    SELECT COLUMN_NAME, DATA_TYPE
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = ?
                """, (table_name,))
                columns = cursor.fetchall()

                for column in columns:
                    column_info = {
                        "name": column.COLUMN_NAME,
                        "type": column.DATA_TYPE
                    }
                    schema_info[table_name].append(column_info)
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection:
            connection.close()

    return schema_info
