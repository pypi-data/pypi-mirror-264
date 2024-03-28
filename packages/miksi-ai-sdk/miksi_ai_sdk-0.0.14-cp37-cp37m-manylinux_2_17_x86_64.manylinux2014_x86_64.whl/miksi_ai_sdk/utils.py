from miksi_ai_sdk.sqltool import get_db_connection

db_name = None
db_user = None
db_password = None
db_host = None
db_port = 3306


def set_db(name, user, password, host, port):
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
    print("Sucess!")
    return f"Success!"

def check_connection(engine):
    # Call get_db_connection and store the return value
    connection_status = get_db_connection(engine, db_user, db_password, db_host, db_port, db_name)
    
    # Return or print the connection status
    return connection_status



def always_clean_json_formatter(answer_text: str) -> str:
    """
    Ensure that the provided answer text is always returned without JSON formatter markers (```json ```).
    This function checks for the presence of these markers and removes them if found,
    without changing the structure of the JSON object within the text.
    """
    # Define the start and end markers for the JSON formatter
    start_marker = "```json"
    end_marker = "```"
    
    # Remove the start and end markers if present, and return the cleaned text
    return answer_text.replace(start_marker, "").replace(end_marker, "").strip()


