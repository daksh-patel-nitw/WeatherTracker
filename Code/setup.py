import mysql.connector
from mysql.connector import Error

def create_table(cursor):
    try:
        # Creating table for user authentication
        query = """
        CREATE TABLE IF NOT EXISTS users (
            u_ID VARCHAR(20) PRIMARY KEY,
            name Varchar(30),
            mobile VARCHAR(15),
            password CHAR(64), 
            security_phrase CHAR(64)
            
        );
        """
        cursor.execute(query)
        
        # Creating table for user authentication
        query = """
           CREATE TABLE IF NOT EXISTS api_usage (
                id INT AUTO_INCREMENT PRIMARY KEY,
                user_id VARCHAR(20),
                last_update TIMESTAMP,
                request_count INT DEFAULT 20,
                FOREIGN KEY (user_id) REFERENCES users(u_ID)
            );
        """
        cursor.execute(query)
        
        # Creating History Table of users
        query = """
        CREATE TABLE IF NOT EXISTS weather_logs (
            id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            location VARCHAR(255),
            temperature VARCHAR(50),
            humidity VARCHAR(50),
            weather_conditions VARCHAR(255),
            wind_speed VARCHAR(50),
            u_ID VARCHAR(20), 
            FOREIGN KEY (u_ID) REFERENCES users(u_ID)
        );
        """
        cursor.execute(query)
        
        
    except Error as e:
        print(f"Error creating table: {e}")

# MySQL database connection setup
def connect_to_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="weather_cli",
            password="password",
            database="python_app_cli"
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error connecting to the database: {e}")
        return None

