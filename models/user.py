from typing import Tuple
from flask import current_app
import psycopg2 as db 
from models.base import BaseModel

class User(BaseModel):
    TABLE_NAME = 'users'
    COLUMN_NAMES = (
        'id',
        'first_name',
        'last_name',
        'username',
        'password',
        'email',
        'birth_date',
        'is_admin',
        'is_banned',
        'date',
    )

    def __init__(self, entry_id=None):
        super().__init__(entry_id)

   
    # this is method that returns first "x" user objects 
    @classmethod
    def get_first_x(cls, id_max):
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE id < %s', (id_max, ))
                list_of_users = []
                for user_tuple in cursor.fetchall():
                    list_of_users.append(User(user_tuple))
                return list_of_users


    #This method returns User object with requested username.
    @classmethod
    def get_from_username(cls, username):
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE username = %s', (username, ))
                if cursor.rowcount == 0:
                    return None
                tuple = (cursor.fetchone())
                u=User(tuple[0])
                print(u.username)
                return User(tuple[0])

    #This method returns true if there is no other user with the same username or email.
    @classmethod
    def unique_user_check(cls, username, email):
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE email = %s OR username = %s', (email,username, ))
                if cursor.rowcount == 0:
                    return True
                else:
                    return False    

    def update_password(self,new_password):
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'UPDATE {self.TABLE_NAME} SET  password = %s WHERE id = %s', (new_password,self.id, ))
                



    
    def render_markdown(self):
        if self.content_type == text:
            # do_something(self.content)s
            pass
          
