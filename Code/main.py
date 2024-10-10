#name--->dsf

from setup import connect_to_db,create_table
import sql_operations as sql
import sys
import re
import os

# To clear the screen after every option is executed.
def cls():
    while input("Press 'y' to clear the screen: ").lower() != 'y':
        print("Please press 'y' to clear the screen.")
    os.system('cls')


class UserApp:
    def __init__(self):
        # Initialize the connection to the database
        self.db = connect_to_db()
        if self.db:
            self.cursor = self.db.cursor()
            create_table(self.cursor)
        self.user_id=""
    
    def __del__(self):
        # Destructor to close the cursor and database connection
        try:
            if self.cursor:
                self.cursor.close()
            if self.db and self.db.is_connected():
                self.db.close()
        except Exception as e:
            print(f"Error during cleanup: {e}")
            
    # Function to reset the password
    def reset_password(self):
        user_id=input("Enter User Id :")
        security_phrase=input("Enter your security_phrase(It might be name of your school, pet, loved_ones) :").strip()
        
        #Authenticating the phrase
        if(sql.authenticate_security_phrase(self.cursor,user_id, security_phrase)):
            pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@!#$%^&*()_+{}\[\]:;"\'<>,.?/~`\\|]).{8,}$'                                
            message = """
            There should be at least one uppercase letter.
            There should be at least one lowercase letter.
            There should be at least one digit.
            There should be at least one special character from the specified set.
            The length of the string should be at least 8 characters.
            """
            while True:
                print(message)
                password=input("Enter new Password (-1 to cancel):").strip()
                if re.fullmatch(pattern, password):
                    sql.change_password(self.cursor, self.db, user_id, password)
                    break
                if(password=="-1"):
                    return
                
        else:
            print("Invalid Security Phrase or User Id.")
    
    #Function to login
    def login(self):
        user_id = input("Enter User Name: ")
        password = input("Enter Password: ")
        
        # Checking the credentials
        if sql.authenticate_password(self.cursor,user_id, password):
            self.user_id=user_id
            print("Login successful!")
            from account import Account
            os.system('cls')
            account_instance = Account(self.user_id,self.cursor,self.db)
            account_instance.account()
        else:
            print("Invalid credentials.")

    #Function to signup
    def signup(self):
        os.system('cls')
        user_id = name= mobile= password= security_phrase=""
        print()
        print("Press -1 to go home.")
        print()
        #Validating unique User_id
        while True:
            user_id = input("Enter Unique User Name: ")
            if user_id=="-1":
                return
            elif sql.user_id_exists(self.cursor,user_id):
                print("ID exists already")
            else:
                break

        #Taking password input
        pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@!#$%^&*()_+{}\[\]:;"\'<>,.?/~`\\|]).{8,}$'                                
        message = """
        There should be at least one uppercase letter.
        There should be at least one lowercase letter.
        There should be at least one digit.
        There should be at least one special character from the specified set.
        The length of the string should be at least 8 characters.
        """
        print(message)

        # Get the new password
        while True:
        
            password = input("Enter new password: ").strip()

            #Password validation
            if re.fullmatch(pattern, password):
                break
            elif(password=="-1"):
                return
            else:
                print(message)
        
        #Confirming the password
        while True:    
            confirm_password=input("Re-Enter the password: ").strip()
            if(confirm_password==password):
                break
            elif(confirm_password=="-1"):
                return
            else:
                print("Passwords didnt match. If  you want to exit, give '-1'")
        
        #Taking the security Phrase
        while True:
            security_phrase=input("Enter security_phrase(It might be name of your school, pet, loved_ones) :").strip()
            if(security_phrase=="-1"):
                print("Security Phrase cannot be '-1'.")
            else:
                break
        
        #Confirming the Security Phrase
        while True:    
            confirm_phrase=input("Re-Enter the Security Phrase: ").strip()
            if(confirm_phrase==security_phrase):
                break
            elif(confirm_phrase=="-1"):
                return
            else:
                print("Security Phrases didnt match. If  you want to exit, give '-1'")
        
        #Taking the name of user
        name=input("Enter name :").strip()
        if(name==-1):
            return
        
        #Pattern for phone number 10 digits
        pattern = r'^\d{10}$'
        #getting the mobile number
        while True:
            mobile=input("Enter Mobile number(10 digits only.):").strip()
            if(mobile==-1):
                return
            if re.fullmatch(pattern, mobile):
                break
            else:
                print("Invalid mobile number.")

                
        sql.add_user_info(self.cursor,self.db,user_id,name,mobile,password,security_phrase)
        print("Successfully Created the account")
        
    #Main Screen login/singnUp
    def login_signup(self):
        os.system('cls')
        print("Welcome to the Street Style Store Weather Application!")
        
        while True:
            print("Options:")
            print("1. Login")
            print("2. Sign Up")
            print("3. Change Password")
            print("4. Exit")
            
            choice = input("Enter your choice: ")

            if choice == "1":
                self.login()
                cls()
            elif choice == "2":
                self.signup()
                cls()
            elif choice == "3":
                self.reset_password()
                cls()
            elif choice == "4":
                print("Exiting...")
                self.cursor.close()
                self.db.close()
                sys.exit()
            else:
                print("Invalid choice. Please try again.\n")
                cls()


if __name__ == "__main__":
    cli = UserApp() #creating instance of app
    cli.login_signup()  # Start the application
