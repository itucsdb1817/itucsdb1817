from flask import current_app, request, jsonify, session
import os
import sys

class User:
    def __init__(self, user_id):
        self.user_id = user_id
        #get_user(user_id)
    def get_user(self, user_id):
        cursor = current_app.config["db"].execute("SELECT * FROM users WHERE id = %(id)s", {'id':user_id})
        if cursor.rowcount == 0:
            current_app.config["db"].close()
            return False
        else:
            for row in cursor:
                self.user_id, self.first_name, self.last_name,self.creation_date,self.birth_date,self.post_karma,self.comment_karma,self.is_admin,self.is_banned,self.username,self.password,self.email = row
                # Initilizes user attributes
                current_app.config["db"].close()
                return True

    def add_user(self, first_name, last_name, birth_date, username, password, email):
        cursor = current_app.config["db"].execute("""INSERT INTO users (
            first_name
            , last_name
            , birth_date
            , username
            , password
            , email
        ) VALUES (    
            %(first_name)s
            , %(last_name)s
            , %(birth_date)s
            , %(username)s
            , %(password)s
            , %(email)s) RETURNING id -- email character varying""", 
            {'first_name':first_name
            , 'last_name':last_name
            , 'birth_date':birth_date
            , 'username':username
            , 'password':password
            , 'email':email})
        fetch = cursor.fetchone()
        print(fetch[0])
        self.get_user(fetch[0])
        current_app.config["db"].close()