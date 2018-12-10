from flask import current_app
import psycopg2 as db
from models.base import BaseModel

class Tag(BaseModel):
    TABLE_NAME = 'tags'
    COLUMN_NAMES = (
        'id',
        'title',
        'date',
        'subscriber_amount'
        'is_banned'
        'description'
        'rules'
    )

    def __init__(self, identifier=None):
        self._DATABASE_CONNECTION = db.connect(current_app.config['DB_URL'])
        # tag id
        if isinstance(identifier, 'int'):
            super.__init__(identifier)
        # tag title
        elif isinstance(identifier, 'str'):
            try:
                with self._DATABASE_CONNECTION.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM {self.__cls__.TABLE_NAME} WHERE title={identifier}"
                    )
                    t = cursor.fetchone()[0]
                    if t is not None:
                        super.__init__(t)
                        return
            except:
                return
    

class TagSubscription(BaseModel):
    TABLE_NAME = 'tag_susbcriptions'
    COLUMN_NAMES = (
        'id',
        'date',
        'user_id',
        'tag_id'
    )

    def __init__(self, entry_id=-1):
        self._DATABASE_CONNECTION = db.connect(current_app.config['DB_URL'])
        if entry_id != -1:
            super().__init__(entry_id)

class TagModerator(BaseModel):
    TABLE_NAME = 'tag_moderators'
    COLUMN_NAMES = (
        'id',
        'date',
        'user_id',
        'tag_id'
    )

    def __init__(self, entry_id=-1):
        self._DATABASE_CONNECTION = db.connect(current_app.config['DB_URL'])
        if entry_id != -1:
            super().__init__(entry_id)