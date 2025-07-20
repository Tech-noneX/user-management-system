from pathlib import Path
import json
import os


class RegisterUser:


    def __init__(self):
        self.path = Path(__file__).parent.joinpath('users_data.json')
        self.menu_super_admin = set()
        self.menu_user = set()
        self.messages = Messages(self)
        self.super_admin_msg = "To register super admin enter 'super admin'."
        self.users_count = 0
        self.users_online = 0
        self.admin = 0
        self.super_admin = 0
        self.super_admin_logged_in = []
        self.admin_logged_in = set()
        self.user_logged_in = set()
        self.users = {}
        self.load_data_from_json()
        self.refresh_data()
        if any(user["role"] == "super admin" for user in self.users.values()):
           self.super_admin_msg = "----Main menu----" 
        

    def main_menu(self):
        commands = ['super admin', 'register', 'log in', 'log out', 'exit',] 
        
        while True:
            print(self.super_admin_msg)
            print("To register new user enter 'register'.")
            print("To log-in enter 'log in'.")
            print("To log-out enter 'log out'.")
            print("To exit enter 'exit'.")
            user = input(":").strip().lower()
            self.input_errors(input=user, list=commands)
            if 'super admin' == user:
                if self.super_admin == 1:
                    print("Super admin has been registered.")
                    continue
                else:        
                    self.new_super_admin()
            if 'register' == user:
                self.new_user()
            if 'log in' == user:
                self.log_in()
            if 'log out' == user:
                self.log_out()
            if 'exit' == user:
                exit()
                

    def new_user(self, attempts= 0, role='user', access= True):
        while True:
            self.nick_name = input("Enter your nickname.\n:")
            if self.nick_name in self.users:
                    print('Nick name already exist')
                    continue
            self.first_name = input("Enter your first name.\n:")
            self.last_name = input("Enter your last name.\n:")
            self.email = input("Enter your email.\n:")
            self.password = input("Enter you password.\n:")
            self.users[self.nick_name] = {
                'first name': self.first_name,
                'last name': self.last_name,
                'email': self.email,
                'password': self.password,
                'role': role,
                'access': access,
                'status': None,
                'attempts': 0,
                'location': None
            }
            self.refresh_data()
            self.save_data_to_json()
            print(f"Number of users registered: {self.users_count}.")
            return


    def new_super_admin(self, role= 'super admin', access= True):
        self.refresh_data()
        print("Register new super admin.")
        self.nick_name = input("Enter your nickname.\n:")
        self.first_name = input("Enter your first name.\n:")
        self.last_name = input("Enter your last name.\n:")
        self.email = input("Enter your email.\n:")
        self.password = input("Enter you password.\n:")
        self.users[self.nick_name] = {
            'first name': self.first_name,
            'last name': self.last_name,
            'email': self.email,
            'password': self.password,
            'role': role,
            'access': access,
            'status': None,
            'attempts': 0,
            'location': None
        }
        print(f"Number of users registered: {self.users_count}.")
        print("Super admin successfully registered.")
        self.super_admin_msg = "---Main menu---"
        print(self.users)
        self.super_admin_menu()
        self.save_data_to_json()


    def log_in(self):
        while True:
            print("----LOG IN----")
            enter_nickname = input("Enter you nick name.\n:")

            if enter_nickname not in self.users:
                print("Invalid nick name")
                continue
            

            if self.users[enter_nickname]['access'] == False:
                print("Access denied contact admin")
                return


            if self.users[enter_nickname]['status'] == 'online':
                print(f"User {enter_nickname} is already logged in.")
                self.menu_user.add(enter_nickname)
                self.users[enter_nickname]['location'] = 'user menu'
                self.save_data_to_json()
                self.user_menu()
                
                if self.users[enter_nickname]['role'] == 'super admin':
                    self.menu_super_admin.add(enter_nickname)
                    print(self.menu_super_admin)
                    self.super_admin_menu()
                

            enter_password = input("Enter your password.\n")
            if enter_password != self.users[enter_nickname]['password']:
                self.users[enter_nickname]['attempts'] += 1
                print("invalid password")
                self.refresh_data()
                self.save_data_to_json()
                if self.users[enter_nickname]['attempts'] == 3:
                    print("Your account has been locked contact 'admin'")
                    self.users[enter_nickname]['access'] = False
                    self.users[enter_nickname]['status'] = 'offline'
                    self.users[enter_nickname]['attempts'] = 0
                    self.refresh_data()
                    self.save_data_to_json()
                    return
                continue

            if enter_password == self.users[enter_nickname]['password']:
                print("Your are logged in")
                print(f"{enter_nickname} is online.")
                self.users[enter_nickname]['status'] = 'online'
                self.users[enter_nickname]['attempts'] = 0
                self.refresh_data()
                self.save_data_to_json()
                if self.users[enter_nickname]['role'] == 'super admin':
                    self.refresh_data()
                    self.menu_super_admin.add(enter_nickname)
                    self.users[enter_nickname]['location'] = 'Super admin menu'
                    self.save_data_to_json()
                    self.super_admin_menu()    
                elif self.users[enter_nickname]['role'] == 'user':
                    self.menu_user.add(enter_nickname)
                    self.users[enter_nickname]['location'] = 'user menu'
                    self.save_data_to_json()
                    self.refresh_data()
                    self.user_menu()
                elif self.users[enter_nickname]['role'] == 'admin':
                    self.save_data_to_json()
                    self.refresh_data()
                    self.admin_menu()
                else:
                    self.refresh_data()
                    self.save_data_to_json()
                    return
                        
            
    def log_out(self):

        while True:
            print("\fLOG-OUT")
            self.refresh_data()
            enter_nickname = input("Enter your nick name.\n:")
            if enter_nickname not in self.users:
                print("Invalid nick name.")
                continue
            if self.users[enter_nickname]['status'] == 'online':
                print(f"{enter_nickname} you have been log out.")
                self.users[enter_nickname]['status'] = 'offline'
                self.refresh_data()
                self.save_data_to_json()
                return
            if self.users[enter_nickname]['status'] == 'offline':
                print("You are already offline.")
                self.refresh_data()
                self.save_data_to_json()
                return


    def super_admin_menu(self):
        
        
        attempts = 0
        commands = ['role', 'access', 'status', 'main menu', 'log out', 'info']
        while True:
            self.refresh_data()
          
            if attempts == 3:
                self.users[self.super_admin_logged_in[0]]['status'] = 'offline'
                self.refresh_data()
                self.main_menu()
            
            print("----Super admin menu----")
            print("To edit role enter 'role'.")
            print("To edit access enter 'access'.")
            print("To edit status enter 'status'.")
            print("To see system info and refresh system enter 'info'")
            print("To go to main menu enter 'main menu'.")
            print("To log out enter 'log out'.")
            
            super_admin_user = input("\n:")
            self.input_errors(input=super_admin_user, list=commands)
            if 'role' == super_admin_user:
                super_admin_user = input("Confirm your password.\n:")
                if self.users[self.super_admin_logged_in[0]]['password'] != super_admin_user:
                    print("!!!Access denied!!!")
                    attempts += 1
                    continue
                nick_name = input("Enter user's nick name.\n:")
                if nick_name in self.super_admin_logged_in:
                    print("You can not change your role.")
                    continue
                change_role = input(f"Change {nick_name}'s role to ('user'/'admin').\n:")
                if self.users[nick_name]['role'] == change_role:
                    print(f"{nick_name}'s role is already {change_role}")
                else:
                    self.users[nick_name]['role'] = change_role
                    print(f"{nick_name}'s role has been changed to {change_role}")
                    self.save_data_to_json()
                    continue
                self.save_data_to_json()
                self.refresh_data()
            if 'main menu' == super_admin_user:
                self.main_menu()

            if 'access' == super_admin_user:
                super_admin_user = input("Confirm your password.\n:")
                if self.users[self.super_admin_logged_in[0]]['password'] != super_admin_user:
                    print("!!!Access denied!!!")
                    attempts += 1
                    continue
                nick_name = input("Enter user's nick name.\n:")
                if nick_name in self.super_admin_logged_in:
                    print("You can not change your access.")
                    continue
                change_access = input(f"Change {nick_name}'s access to ('True'/'False').\n:").lower()
                if 'true' == change_access:    
                    self.users[nick_name]['access'] = True
                    print(f"{nick_name}'s access has been changed to {True}.")
                    self.refresh_data()
                    self.save_data_to_json()
                    continue
                else:
                    self.users[nick_name]['access'] = False
                    self.users[nick_name]['status'] = 'offline'
                    print(f"{nick_name}'s access has been changed to {False}.\n"
                          f"{nick_name} account has been locked."                    
                    )
                    self.refresh_data()
                    self.save_data_to_json()
                    continue
            if 'status' == super_admin_user:
                super_admin_user = input("Confirm your password.\n:")
                if self.users[self.super_admin_logged_in[0]]['password'] != super_admin_user:
                    print("!!!Access denied!!!")
                    attempts += 1
                    continue
                nick_name = input("Enter user's nick name.\n:")
                if nick_name in self.super_admin_logged_in:
                    print("You can not change your status.")
                    continue
                change_status = input(f"Change {nick_name}'s status to ('online'/'offline').\n:")
                if self.users[nick_name]['status'] == change_status:
                    print(f"{nick_name}'s role is already {change_status}")
                else:
                    self.users[nick_name]['status'] = change_status
                    print(f"{nick_name}'s status has been changed to {change_status}")
                    self.refresh_data()
                    self.save_data_to_json()
            if 'log out' == super_admin_user:
                while True:
                    self.refresh_data()
                    print("\fLOG-OUT")
                    enter_nickname = input("Enter your nick name.\n:")
                    if enter_nickname not in self.super_admin_logged_in:
                        print("Invalid nick name.")
                        continue
                    if self.users[enter_nickname]['status'] == 'offline':
                        print(f"{enter_nickname} is not logged in")
                        self.main_menu()
                    if enter_nickname in self.super_admin_logged_in:
                        self.users[enter_nickname]['status'] = 'offline'
                        self.super_admin_logged_in.remove(enter_nickname)
                        print("----You logged out----")
                        self.exit_location(nick_name=enter_nickname,from_menu=self.menu_super_admin)
                        self.refresh_data()
                        self.save_data_to_json()
                        exit()
            if 'info' == super_admin_user:
                self.admin_refresh_data()
                continue   
        #if super_admin_user not in commands:
                #print("Invalid input")


    def user_menu(self):
        commands = ['message', 'edit', 'password', 'log out', 'exit']
        while True:
            print("----user menu----")
            print("To send message enter 'message'.")
            print("To edit personal details enter 'edit'.")
            print("To change password enter 'password'.")
            print("To log out enter 'log out'.")
            print("To exit enter 'exit'.")
            user = input(":")
            self.input_errors(input=user, list=commands)
            if 'message' in user:
                self.messages.send_message()
            if 'exit' in user:
                nick_name = input("Enter your nick name.\n")
                if nick_name not in self.menu_user:
                    print("Invalid nick name")
                    continue
                self.users[nick_name]['status'] = 'offline'
                self.exit_location(nick_name=nick_name,from_menu=self.menu_user)
                self.save_data_to_json()
                exit()
                

    def admin_menu(self):
        self.admin_menu_list = []
        commands = ['message', 'edit', 'password', 'status', 'access']
        while True:
            print("----admin menu----")
            print("To send message enter 'message'.")
            print("To edit personal details enter 'edit'.")
            print("To change password enter 'password'.")
            print("To change user's status enter 'status'.")
            print("To change user's access enter 'access'.")
            user = input(":")
            self.input_errors(input=user, list=commands)


    def save_data_to_json(self):
        try:
            with open(self.path, "w") as file:
                json.dump(self.users, file, indent= 4)
            print("User data has been saved to 'users_data.json'.")
        except Exception as e:
            print(f"Error saving user data: {e}")    


    def load_data_from_json(self):
        if self.path.exists():
            with open(self.path, "r") as file:
                self.users = json.load(file)
            print("User data loaded from users_data.json")
        else:
            print("No existing data found starting fresh.")


    def refresh_data(self):
        self.users_count = 0
        self.users_online = 0
        self.super_admin = 0
        self.admin = 0

        self.super_admin_logged_in = []
        self.admin_logged_in = set()
        self.user_logged_in = set()
        for user in self.users.items():
            self.users_count += 1
        for values in self.users.values():
            if values['status'] == 'online':
                self.users_online += 1
        for values in self.users.values():
            if values['role'] == 'admin':
                self.admin += 1
        for values in self.users.values():
            if values['role'] == 'super admin':
                self.super_admin += 1
        for nick, data in self.users.items():
            if data['role'] == 'super admin':
                if data['status'] == 'online':
                    self.super_admin_logged_in.append(nick)       
        for nick, data in self.users.items():
            if data['role'] == 'admin':
                if data['status'] == 'online':
                    self.admin_logged_in.add(nick)
        for nick, data in self.users.items():
            if data['role'] == 'user':
                if data['status'] == 'online':
                    self.user_logged_in.add(nick)


    def admin_refresh_data(self):
        self.users_count = 0
        self.users_online = 0
        self.super_admin = 0
        self.admin = 0

        self.super_admin_logged_in = []
        self.admin_logged_in = set()
        self.user_logged_in = set()
        for user in self.users.items():
            self.users_count += 1
        for values in self.users.values():
            if values['status'] == 'online':
                self.users_online += 1
        for values in self.users.values():
            if values['role'] == 'admin':
                self.admin += 1
        for values in self.users.values():
            if values['role'] == 'super admin':
                self.super_admin += 1
        for nick, data in self.users.items():
            if data['role'] == 'super admin':
                if data['status'] == 'online':
                    self.super_admin_logged_in.append(nick)       
        for nick, data in self.users.items():
            if data['role'] == 'admin':
                if data['status'] == 'online':
                    self.admin_logged_in.add(nick)
        for nick, data in self.users.items():
            if data['role'] == 'user':
                if data['status'] == 'online':
                    self.user_logged_in.add(nick)
        print(f"Number of users registered: {self.users_count}\n"
              f"Number of users 'online': {self.users_online}\n"
              f"Number of admins registered: {self.admin}\n"
              f"Number of super admins registered {self.super_admin}\n")
        print("Super admin online:")
        for nick_name in self.super_admin_logged_in:
            print(nick_name)      
        print("Admins online:")
        for nick_name in self.admin_logged_in:
            print(nick_name)
        print("Users online:")
        for nick_name in self.user_logged_in:
            print(nick_name)     
        print("Accounts locked:")
        for nick, data in self.users.items():
            if data['access'] == False:
                print(nick)


    def input_errors(self, input, list):
        if input not in list:
            print("---Invalid input---.")
            return


    def update_dictionary(self):
        for key, value in self.users.items():
            if 'location' not in value:
                value['location'] = None
                self.save_data_to_json()


    def update_location(self, nick_name, from_menu, to_menu, location):
        self.users[nick_name]['location'] = location
        from_menu.remove(nick_name)
        to_menu.append(nick_name)
        

    def exit_location(self, nick_name, from_menu, location=None):
        self.users[nick_name]['location'] = location
        from_menu.remove(nick_name)
        



class Messages:


    def __init__(self, register_user_instance):
        self.ru = register_user_instance
        #for user in self.ru.users['users']:
            #print(user)
        

    def send_message(self):
        print("coming soon")
        for user in self.ru.users:
            print(user)

RegisterUser().main_menu()





        
        