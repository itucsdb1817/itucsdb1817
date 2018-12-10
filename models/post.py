from typing import Tuple
from flask import current_app
import psycopg2 as db 
from models.base import BaseModel

# possible content types:
# Internal: (uploaded to site)
#   text
#   video
#   picture
# External: (Must be all links)
#   un-renderable link
#   video
#   picture

class Post(BaseModel):
    TABLE_NAME = 'posts'
    COLUMN_NAMES = (
        'id',
        'user_id',
        'date',
        'title',
        'content_type',
        'content',
        'is_external',
        'current_vote',
        'rank_score',
        'is_banned',
        'comment_count',
        'tag_id'
    )
    def __init__(self, entry_id=-1):
        # each instance of object has a connection of its own that get closed automatically
        # when the object goes out of scope
        self._DATABASE_CONNECTION = db.connect(current_app.config['DB_URL'])
        if entry_id != -1:
            super().__init__(entry_id)

    ## NEW FUNCTIONS HERE
    # RULE OF THUMB:
    #       IF YOU NEED TO ACCESS COLUMN VALUES, USE NORMAL METHODS

    # UTILITY METHODS
    # these utility methods are called from the class, not instance
    # they are related to the table, but does not necessarly require the values of an instance
    # these methods at most need the TABLE_NAME or COLUMN_NAMES from the class and nothing else
    # Utility methods should create their own database connections if needed
    # eg: Get first x entries in table posts as objects , 
    # WILL WORK:    obj = Post()
    #               obj.example()
    # PREFERED:     Post.example()

    # this is method that returns a list of post objects
    @classmethod
    def get_first_x(cls, id_max):
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE id < %s', (id_max, ))
                list_of_posts = []
                for post_tuple in cursor.fetchall():
                    list_of_posts.append(Post(post_tuple))
                return list_of_posts
    
    @classmethod
    def get_user_post(cls,user_id):             
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE user_id = %s', (user_id, ))
                list_of_posts = []
                for post_tuple in cursor.fetchall():
                    list_of_posts.append(Post(post_tuple))
                return list_of_posts
