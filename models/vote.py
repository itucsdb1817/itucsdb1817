from typing import Tuple
from flask import current_app
import psycopg2 as db 
from models.base import BaseModel



class Vote(BaseModel):
    TABLE_NAME = 'votes'
    COLUMN_NAMES = (
        'id',
        'user_id' ,
        'date',
        'is_comment',
        'vote' ,
        'vote_ip',
        'last_update_time',
        'post_id',
        'comment_id'
    )

    def __init__(self, entry_id=None):
        super().__init__(entry_id)

    
    @classmethod
    def get_user_post_vote(cls,user_id,post_id):             
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE user_id = %s AND post_id = %s', (user_id,post_id, ))
                list_of_votes = []
                for vote_tuple in cursor.fetchall():
                    list_of_votes.append(Vote(vote_tuple))
                return list_of_votes

    @classmethod
    def get_user_comment_vote(cls,user_id,comment_id):             
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE user_id = %s AND comment_id = %s', (user_id,comment_id, ))
                list_of_votes = []
                for vote_tuple in cursor.fetchall():
                    list_of_votes.append(Vote(vote_tuple))
                return list_of_votes

    @classmethod
    def get_user_total_votes(cls,user_id):             
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE user_id = %s', (user_id, ))
                list_of_votes = []
                for vote_tuple in cursor.fetchall():
                    list_of_votes.append(Vote(vote_tuple))
                return list_of_votes
                
