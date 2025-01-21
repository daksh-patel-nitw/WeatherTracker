from setup import connect_to_db
from mysql.connector import Error
import hashlib
from datetime import datetime,timedelta

#Function to encode password and Security_Phrase
def hash_sha256(data):
    return hashlib.sha256(data.encode()).hexdigest()

# Function to add data to the database
def add_user_info(cursor, db,id,name,mobile,password,security_phrase):
    try:
        if(id is None):
            print("Error: no user ID found.")
            return
        if(name is None):
            print("Error: no user Name found.")
            return
        if(mobile is None):
            print("Error: no user Mobile found.")
            return
        if(password is None):
            print("Error: no user Password found.")
            return
        if(security_phrase is None):
            print("Error: no Security phrase for User found.")
            return
        #converting the password to sha256 HASH
        password=hash_sha256(password)
        security_phrase=hash_sha256(security_phrase)
        query = "INSERT INTO users (u_ID, name, mobile, password, security_phrase) VALUES (%s, %s, %s, %s, %s)"
        values = (id,name,mobile,password,security_phrase)
        cursor.execute(query, values)
        db.commit()
        
        
        
        #adding the api count to track the usage
        last_update = datetime.now()
        # Initial request_count is already set to 20
        query = "INSERT INTO api_usage (user_id, last_update) VALUES (%s, %s)"
        values = (id, last_update)  
        
        cursor.execute(query, values)
        db.commit()
        
        print("Data added successfully!")
    except Error as e:
        print(f"Error adding data to the database: {e}")
        db.rollback()  # Rollback in case of error

# Function to retrieve data from the database
def get_user_info(cursor, id):
    try:
        # Correct query syntax and use parameterized query
        query = "SELECT * FROM users WHERE u_ID = %s"
        cursor.execute(query, (id,))
        result = cursor.fetchall()
        
        # Check if any data was retrieved
        if result:
            print()
            print("\t\t\t","-" * 40)
            for row in result:
                print(f"\t\t\t\tID \t:{row[0]}\n\t\t\t\tName \t:{row[1]}\n\t\t\t\tMobile \t:{row[2]}")
            print("\t\t\t","-" * 40)
            print()
        else:
            print("No user found with the provided ID.")
    except Error as e:
        print(f"Error retrieving data from the database: {e}")

#Function to check if the user id already exists.            
def user_id_exists(cursor, user_id):
    try:
        query = "SELECT COUNT(*) FROM users WHERE u_ID = %s"
        cursor.execute(query, (user_id,))
        count = cursor.fetchone()[0]
        return count > 0
    except Error as e:
        print(f"Error checking user ID existence: {e}")
        return False

# Check the user and password authentication
def authenticate_password(cursor,user_id, password):
    try:
        query = "SELECT password FROM users WHERE u_ID = %s"
        cursor.execute(query, (user_id,))
        #Here if user id is wrong then we get error
        try:
            saved_password = cursor.fetchone()[0]
        except:
            return False
        password=hash_sha256(password)
        return password==saved_password
    except Error as e:
        print(f"Error checking user ID existence: {e}")
        return False

#change the password
def change_password(cursor, db, user_id, password):
    try:
        password=hash_sha256(password)
        query = "UPDATE users SET password = %s WHERE u_ID = %s"
        values = (password, user_id)
        cursor.execute(query, values)
        
        db.commit()
        
        print("Password Changed Successfully. ")
    except Error as e:
        print(f"Error changing the password from the database: {e}")
        db.rollback()
        
#Check if the user has entered the correct security
def authenticate_security_phrase(cursor,user_id, security_phrase):
    try:
        query = "SELECT security_phrase FROM users WHERE u_ID = %s"
        cursor.execute(query, (user_id,))
        #Here if user id is wrong then we get error
        try:
            saved_security_phrase = cursor.fetchone()[0]
        except:
            return False
        security_phrase=hash_sha256(security_phrase)
        return security_phrase==saved_security_phrase
    except Error as e:
        print(f"Error checking user ID existence: {e}")
        return False

#fetch the API Count and also update the api count to 20 if 24 hours have passed.
def get_api_usage(cursor, db, user_id):
    try:
        # Query to fetch the request count and last_update timestamp for the specified user
        query =" SELECT request_count, last_update FROM api_usage WHERE user_id = %s "
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        
        current_time = datetime.now()
    
        request_count, last_update = result
            
            # Check if the last_update is more than 24 hours old
        if current_time - last_update > timedelta(hours=24):
            # Update the record with new timestamp and reset count to 20
            update_query = "UPDATE api_usage SET last_update = %s, request_count = 20 WHERE user_id = %s"
            cursor.execute(update_query, (current_time, user_id))
            db.commit()
            return 5  # Return the updated request count
        else:
            return request_count  # Return the existing request count
        

    except Error as e:
        print(f"Error retrieving API usage data: {e}")
        return None

#Decrease the api count
def decrease_api_count(cursor, db, user_id):
    try:
        # Fetch the current request count for the user
        query = """
            SELECT request_count
            FROM api_usage
            WHERE user_id = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        
        if result:
            current_count = result[0]
            new_count = current_count - 1
                
            update_query = """
                    UPDATE api_usage
                    SET request_count = %s
                    WHERE user_id = %s
            """
            cursor.execute(update_query, (new_count, user_id))
            db.commit()
            print("API count decreased successfully!")
        else:
            print("No record found for the user.")
    except Error as e:
        print(f"Error decreasing API count: {e}")
        db.rollback()  # Rollback in case of error
   
#Function to log history
def add_weather_log(cursor, db, user_id, location, temperature, humidity, weather_conditions, wind_speed):
    try:
        query = """
        INSERT INTO weather_logs (u_ID, location, temperature, humidity, weather_conditions, wind_speed)
        VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (user_id, location, temperature, humidity, weather_conditions, wind_speed)
        cursor.execute(query, values)
        db.commit()
        print()
        print("\t\t\t","-" * 40)
        print("\t\t\t\tCurrent Temperature\t:", temperature)
        print("\t\t\t\tHumidity\t\t:", humidity)
        print("\t\t\t\tWeather_Conditions\t:", weather_conditions)
        print("\t\t\t\tWind_speed\t\t:", wind_speed)
        print("\t\t\t","-" * 40)
        print()
        # print("Weather log added successfully!")
    except Error as e:
        print(f"Error adding weather log: {e}")
        db.rollback()

#Fetch weather logs to of the current user
def get_weather_logs(cursor, user_id):
    try:
        query = """
        SELECT wl.id, wl.timestamp, wl.location, wl.temperature, wl.humidity, wl.weather_conditions, wl.wind_speed
        FROM weather_logs wl
        INNER JOIN users u ON wl.u_ID = u.u_ID
        WHERE wl.u_ID = %s
        """
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        print()
        print("-" * 120)
        if result:
            
            print("ID\t\tTimestamp\t\tLocation\tTemperature\tHumidity\tWeather Conditions\tWind Speed")
            print("-" * 120)
            for row in result:
                print(f"{row[0]}\t\t{row[1]}\t{row[2]}\t{row[3]}\t\t{row[4]}\t\t{row[5]}\t\t{row[6]}")
            
        else:
            print("\t\t\t\tNo data found for the given user ID.")
            return
        print("-" * 120)
        print()
            
    except Error as e:
        print(f"Error retrieving data: {e}")

#Remove weather logs of the current user
def remove_weather_logs(cursor, db, user_id, id):
    try:
        query = """
            DELETE FROM weather_logs
            WHERE id = %s AND u_ID = %s
        """
        cursor.execute(query, (id, user_id))
        db.commit()
        if cursor.rowcount > 0:
            print("Row deleted successfully!")
        else:
            print("No row found with the given id and user_id.")
    except Error as e:
        print(f"Error deleting data from the database: {e}")
        db.rollback()
