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

    def __init__(self, entry_id=-1):
        self._DATABASE_CONNECTION = db.connect(current_app.config['DB_URL'])
        if entry_id != -1:
            super().__init__(entry_id)
    
