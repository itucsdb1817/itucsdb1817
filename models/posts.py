from typing import Tuple
from flask import current_app
import psycopg2 as db 
from base import BaseModel

# NOT FINAL
# MAY BE SUBJECTED TO CHANGE
class Post(BaseModel):
    def __init__(self, entry_id=-1):
        # each instance of object has a connection of its own that get closed automatically
        # when the object goes out of scope
        self._DATABASE_CONNECTION = db.connect(current_app.config['db'])
        self._TABLE_NAME = 'posts'
        self._COLUMN_NAMES = (
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
        if entry_id != -1:
            super().__init__(entry_id)


    def save():
        raise NotImplementedError()
    ## NEW FUNCTIONS HERE