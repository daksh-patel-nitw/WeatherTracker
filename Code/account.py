from main import UserApp
import sql_operations as sql
from weather import getData
import os

# To clear the screen after every option is executed.
def cls():
    while input("Press 'y' to clear the screen: ").lower() != 'y':
        print("Please press 'y' to clear the screen.")
    os.system('cls')


#This class is used for users interaction of his/her account.
class Account(UserApp):
    def __init__(self, user_id,cursor,db):
        super().__init__()
        self.user_id = user_id
        self.db = db
        self.cursor = cursor
    
    #It is used to display the profile of the user
    def profile(self):
        sql.get_user_info(self.cursor, self.user_id)
    
    #It is used to fetch the weather data
    def weather_info(self):
        location=input("Enter City/Country/State name :")
        temperature, humidity, weather_conditions, wind_speed=getData(location)
        sql.decrease_api_count(self.cursor,self.db,self.user_id)
        if(temperature is not None and humidity is not None and weather_conditions is not None and wind_speed is not None):
            sql.add_weather_log(self.cursor, self.db, self.user_id, location, temperature, humidity, weather_conditions, wind_speed)
    
    # It is used to show the history of the weather data.
    def history(self):
        sql.get_weather_logs(self.cursor,self.user_id)
    
    # It is used to remove history with specific id.
    def remove_history(self):
        id=input("Enter id :")
        sql.remove_weather_logs(self.cursor, self.db, self.user_id, id)
    
    #This is the main looping function.
    def account(self):
        print(f"\nWelcome to your account, {self.user_id}!\n")
        
        while True:
            api_count=sql.get_api_usage(self.cursor,self.db,self.user_id)
            print(api_count," out of 20 Api Calls left")
            print("\nOptions:")
            print("1. View Profile")
            print("2. Get Current Weather Info by City/Country/State name")
            print("3. View History")
            print("4. Remove from History")
            print("5. Log out")
            
            choice = input("Enter your choice: ")

            if choice == "1":
                self.profile()
                cls()
            elif choice == "2":
                api_count=sql.get_api_usage(self.cursor,self.db,self.user_id)
                if api_count and api_count > 0:
                    self.weather_info()
                else:
                    print("\n Insufficient API Counts.")
                cls()
            elif choice == "3":
                self.history()
                cls()
            elif choice == "4":
                self.remove_history()
                cls()
            elif choice == "5":
                print("Logging out...")
                return
            else:
                print("Invalid choice. Please try again.\n")
                cls()