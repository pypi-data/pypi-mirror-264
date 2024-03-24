import sqlite3
import os
import shutil
from datetime import datetime

def get_primary_key_columns(filepath: str, table_name: str) -> list:
    """
    Get the names of the primary key columns in a SQLite database table.

    Parameters:
        - filepath (str): The full path including the filename of the SQLite database file.
        - table_name (str): The name of the table.

    Returns:
        - list: A list containing the names of the primary key columns.
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()
        
        # Get primary key columns
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()
        primary_key_columns = [col[1] for col in columns_info if col[5] == 1]  # column[5] indicates if column is primary key
        
        # Close connection
        conn.close()
        
        return primary_key_columns
    
    except Exception as e:
        print(f"Error retrieving primary key columns: {e}")
        return []


def create_sqlite_db(path:str, filename:str, key:str, columns:str, overwrite:bool=False) -> bool:
    """
    Create a SQLite database with the specified parameters.

    Parameters:
        - path (str): The directory path where the database will be created.
        - filename (str): The name of the SQLite database file.
        - key (str): A key value.
        - columns (str): A comma-separated string specifying the columns for the table.
        - overwrite (bool, optional): Whether to allow overwriting if the file already exists. Defaults to False.

    Returns:
        - bool: True if the database was successfully created or False if an error occurred or overwrite is False and the file already exists.
    
    Example:
        - create_sqlite_db(path="/path/to/database", filename="example.db", key="my_key", columns="column1 TEXT, column2 INTEGER", overwrite=True)
    """    
    full_path = os.path.join(path, filename)
    
    # Check if the file already exists
    if os.path.exists(full_path):
        if not overwrite:
            return False
        else:
            os.remove(full_path)  # Delete the existing database file
    
    # Connect to SQLite database
    conn = sqlite3.connect(full_path)
    cursor = conn.cursor()
    
    key_exists = any(col.split()[0] == key.split()[0] for col in columns.split(','))
    if not key_exists:
        columns = f"{key}, {columns}"
    
    # Create table with columns and primary key
    try:
        cursor.execute(f"CREATE TABLE IF NOT EXISTS data ({columns}, PRIMARY KEY ({key.split()[0]}))")
        conn.close()
        return True    
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")
        conn.close()
        return False

def delete_sqlite_db(filepath: str, confirm: bool = False) -> bool:
    """
    Delete a SQLite database file.

    Parameters:
        - filepath (str): The full path including the filename of the SQLite database file to delete.
        - confirm (bool, optional): Whether to ask for manual confirmation before deleting. Defaults to False.

    Returns:
        - bool: True if the database file was successfully deleted, False otherwise.
    
    Example: 
        - delete_sqlite_db("/path/to/database/example.db", confirm=True)
    """
    # Check if the file exists
    if not os.path.exists(filepath):
        print("File does not exist.")
        return False
    
    # Ask for confirmation if confirm is True
    if confirm:
        user_input = input("Are you sure you want to delete the database file? (Y/N): ").strip().upper()
        if user_input != "Y":
            print("Operation canceled.")
            return False
    
    # Attempt to delete the file
    try:
        os.remove(filepath)
        return True
    except Exception as e:
        print(f"Error deleting database file: {e}")
        return False

def add_to_database(filepath: str, keyvalue: str, data: list) -> bool:
    """
    Add data to a SQLite database.

    Parameters:
        - filepath (str): The full path including the filename of the SQLite database file.
        - keyvalue (str): The key value identifying the data to be added.
        - data (list): A list of dictionaries, where each dictionary contains the data to be added to the database. 
                       The keys should match the column names in the database table.

    Returns:
        - bool: True if the data was successfully added, False otherwise.
    
    Example: 
        - add_to_database("/path/to/database/example.db", "id", [{"id": 1, "name": "John", "age": 30}, {"id": 2, "name": "Jane", "age": 25}])
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()
        
        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='data'")
        table_exists = cursor.fetchone()
        if not table_exists:
            print("Table 'data' does not exist.")
            conn.close()
            return False
        
        # Prepare data for insertion
        columns = ', '.join(data[0].keys())
        values = ', '.join(['?' for _ in data[0].values()])
        query = f"INSERT INTO data ({columns}) VALUES ({values})"
        
        # Execute query for each tuple
        for entry in data:
            cursor.execute(query, list(entry.values()))
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error adding data to database: {e}")
        return False

def edit_database_data(filepath: str, keyvalue: str, data: dict, table_name: str = "data") -> bool:
    """
    Edit data in a SQLite database.

    Parameters:
        - filepath (str): The full path including the filename of the SQLite database file.
        - keyvalue (str): The value used to uniquely identify the tuple to be edited.
        - data (dict): A dictionary containing the updated data. 
                       The keys should match the column names in the database table.
        - table_name (str): The name of the table in the database. Defaults to "data".

    Returns:
        - bool: True if the data was successfully edited, False otherwise.
    
    Example:
        - edit_database_data(filepath="/path/to/database/example.db", keyvalue="123", 
                             data={"name": "New Name", "age": 35}, table_name="users")
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()
        
        # Get primary key columns
        primary_key_columns = get_primary_key_columns(filepath, table_name)
        if not primary_key_columns:
            print("Error: No primary key columns found.")
            conn.close()
            return False
        
        # Prepare data for update
        update_columns = ', '.join([f"{key} = ?" for key in data.keys()])
        where_clause = ' AND '.join([f"{key} = ?" for key in primary_key_columns])
        query = f"UPDATE {table_name} SET {update_columns} WHERE {where_clause}"
        
        # Execute query
        cursor.execute(query, list(data.values()) + [keyvalue])
        
        # Commit changes and close connection
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error editing data in database: {e}")
        return False

def overwrite_database(filepath: str, data: list, table_name: str = "data") -> bool:
    """
    Overwrite the contents of a SQLite database with a list of data tuples,
    ensuring that only tuples with unique key values are appended.

    Parameters:
        - filepath (str): The full path including the filename of the SQLite database file.
        - data (list): A list of dictionaries, where each dictionary contains the data to be added to the database. 
                       The keys should match the column names in the database table.
        - table_name (str): The name of the table in the database. Defaults to "data".

    Returns:
        - bool: True if the database was successfully overwritten, False otherwise.
    
    Example:
        - overwrite_database(filepath="/path/to/database/example.db",
                             data=[{"id": 1, "name": "John", "age": 30},
                                   {"id": 2, "name": "Jane", "age": 25}],
                             table_name="users")
    """
    try:
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()
        cursor.execute(f"DELETE FROM {table_name}")
        primary_key_columns = get_primary_key_columns(filepath, table_name)
        columns = ', '.join(data[0].keys())
        placeholders = ', '.join(['?' for _ in data[0].values()])
        query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
        for entry in data:
            if not primary_key_columns or all(entry[key] != None for key in primary_key_columns):
                cursor.execute(query, tuple(entry.values()))
        conn.commit()
        conn.close()
        return True

    except Exception as e:
        print(f"Error overwriting database: {e}")
        return False

def load_data_by_key(filepath: str, keyvalue: str, table_name: str = "data") -> dict:
    """
    Load specific data from a SQLite database based on a key value.

    Parameters:
        - filepath (str): The full path including the filename of the SQLite database file.
        - keyvalue (str): The value used to uniquely identify the tuple to be loaded.
        - table_name (str): The name of the table in the database. Defaults to "data".

    Returns:
        - dict: A dictionary containing the loaded data, or an empty dictionary if no data was found.
    
    Example:
        - data = load_data_by_key(filepath="/path/to/database/example.db", keyvalue="123", table_name="users")
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()
        
        # Get column names
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns = [col[1] for col in cursor.fetchall()]
        
        # Prepare query
        query = f"SELECT * FROM {table_name} WHERE id = ?"
        
        # Execute query
        cursor.execute(query, (keyvalue,))
        result = cursor.fetchone()
        
        # Close connection
        conn.close()
        
        if result:
            return dict(zip(columns, result))
        else:
            print("No data found for the specified key.")
            return {}

    except Exception as e:
        print(f"Error loading data from database: {e}")
        return {}

def load_all_data(filepath: str, table_name: str = "data") -> list:
    """
    Load all data from a SQLite database table, including the key value.

    Parameters:
        - filepath (str): The full path including the filename of the SQLite database file.
        - table_name (str): The name of the table in the database. Defaults to "data".

    Returns:
        - list: A list of tuples, where each tuple represents a row of data from the database table.
    
    Example:
        - data = load_all_data(filepath="/path/to/database/example.db", table_name="users")
    """
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()
        
        # Prepare query
        query = f"SELECT * FROM {table_name}"
        
        # Execute query
        cursor.execute(query)
        result = cursor.fetchall()
        
        # Close connection
        conn.close()
        
        return result

    except Exception as e:
        print(f"Error loading data from database: {e}")
        return []

def backup_database(filepath: str, backup_dir: str) -> bool:
    """
    Create a backup of a SQLite database file with the current date appended to the filename.

    Parameters:
        - filepath (str): The full path including the filename of the SQLite database file.
        - backup_dir (str): The directory path where the backup file will be created.

    Returns:
        - bool: True if the backup was successful, False otherwise.
    
    Example:
        - backup_database(filepath="/path/to/database/example.db", backup_dir="/path/to/backup")
    """
    try:
        current_datetime = datetime.now()
        date_str = current_datetime.strftime("%Y-%m-%d_%H-%M-%S")
        backup_filename = f"{date_str}_{os.path.basename(filepath)}"
        backup_filepath = os.path.join(backup_dir, backup_filename)
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
        shutil.copy(filepath, backup_filepath)
        return True
    
    except Exception as e:
        print(f"Error creating database backup: {e}")
        return False

def rename_database(filepath: str, new_filename: str) -> bool:
    """
    Rename a SQLite database file.

    Parameters:
        - filepath (str): The full path including the filename of the SQLite database file.
        - new_filename (str): The new filename for the database file.

    Returns:
        - bool: True if the database was successfully renamed, False otherwise.
    
    Example:
        - rename_database(filepath="/path/to/database/example.db", new_filename="new_database.db")
    """
    try:
        directory, current_filename = os.path.split(filepath)
        new_filepath = os.path.join(directory, new_filename)
        os.rename(filepath, new_filepath)
        return True
    
    except Exception as e:
        print(f"Error renaming database: {e}")
        return False

    
def remove_data_by_key(filepath: str, keyvalues: list, table_name: str = "data") -> bool:
    """
    Remove data from a SQLite database based on a list of key values.

    Parameters:
        - filepath (str): The full path including the filename of the SQLite database file.
        - keyvalues (list): A list of values used to uniquely identify the tuples to be removed.
        - table_name (str): The name of the table in the database. Defaults to "data".

    Returns:
        - bool: True if the data was successfully removed, False otherwise.
    
    Example:
        - remove_data_by_key(filepath="/path/to/database/example.db", keyvalues=["123", "456"], table_name="users")
    """

    try:
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()
        query = f"DELETE FROM {table_name} WHERE id = ?"
        
        # Execute the deletion query for each key value
        for keyvalue in keyvalues:
            cursor.execute(query, (keyvalue,))
        
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error removing data from database: {e}")
        return False
    
def purge_db_data(filepath: str, table_name: str = "data", confirm: bool = False) -> bool:
    """
    Clear the data from a SQLite database table.

    Parameters:
        - filepath (str): The full path including the filename of the SQLite database file.
        - table_name (str): The name of the table in the database. Defaults to "data".
        - confirm (bool): Whether to prompt for confirmation before clearing the data. Defaults to True.

    Returns:
        - bool: True if the data was successfully cleared, False otherwise.
    
    Example:
        - purge_db_data(filepath="/path/to/database/example.db", table_name="users", confirm=True)
    """
    try:
        if confirm:
            user_input = input(f"Are you sure you want to clear all data from the '{table_name}' table? (yes/no): ")
            if user_input.lower() != 'yes':
                print("Operation cancelled.")
                return False
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()
        query = f"DELETE FROM {table_name}"
        cursor.execute(query)
        conn.commit()
        conn.close()
        return True
    
    except Exception as e:
        print(f"Error clearing data from database: {e}")
        return False
    
def check_if_key_exists(filepath: str, keyvalue: str, table_name: str = "data") -> bool:
    """
    Check if a row with the specified key value exists in the SQLite database.

    Parameters:
        - filepath (str): The full path including the filename of the SQLite database file.
        - keyvalue (str): The value of the key to check.
        - table_name (str): The name of the table in the database. Defaults to "data".

    Returns:
        - bool: True if a row with the specified key value exists, False otherwise.
    
    Example:
         check_key_exists(filepath="/path/to/database/example.db", keyvalue="123", table_name="users")
    """
    try:
        conn = sqlite3.connect(filepath)
        cursor = conn.cursor()
        query = f"SELECT 1 FROM {table_name} WHERE id = ?"
        cursor.execute(query, (keyvalue,))
        row = cursor.fetchone()
        conn.close()
        return bool(row)
    except Exception as e:
        print(f"Error checking if key exists in database: {e}")
        return False