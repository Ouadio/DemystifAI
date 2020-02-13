# -*- coding: utf-8 -*-

from flowers_recogn.user import User

users = [User(1,'admin1', 'admin1'), User(2,'admin2','admin2')]


username_table = {u.username : u for u in users}
userid_table = {u.id : u for u in users}



def authenticate(username, password):
    myUser = username_table.get(username, None) #returns None if the username is not there
    if myUser and myUser.password==password:
        return(myUser)
        
        
def identity(payload):
    user_id = payload['identity']
    return(userid_table.get(user_id, None))