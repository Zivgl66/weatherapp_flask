from pymongo import MongoClient
import bcrypt 
import os

client = MongoClient(os.environ.get('DB_URI'), connect=False)
db = client.WeatherApp
users = db.users

def add_user_to_db(username, password):
# This function checks if a user already exists in the DB and return True/False
    if username != '' and len(username) >= 3:
        print(users.find_one({"username": username}))
        if users.find_one({"username": username}):
            return False    
        else: 
            # converting password to array of bytes 
            bytes = password.encode('utf-8') 
            
            # generating the salt 
            salt = bcrypt.gensalt() 
            
            # Hashing the password 
            hash = bcrypt.hashpw(bytes, salt) 
            user = {'username': username, 'password': hash}
            user_id = users.insert_one(user).inserted_id
            print(user_id)
    # collection.insert_one({'username': username, 'password': password})
            return True
    else:
        return False
    

def login_user_from_db(username, password):
# This function checks if a user exists in the DB and if so, compares hashed passwords
# and return True/False
    user = users.find_one({"username": username})
    if user:
        print(user)
        userBytes = password.encode('utf-8') 
        if bcrypt.checkpw(userBytes, user['password']):
            return True
    return False
        
            
            
