from flask import current_app
import psycopg2 as db
from models.base import BaseModel
from models.user import User

class Comment(BaseModel):
    TABLE_NAME = 'comments'
    COLUMN_NAMES = (
        'id',
        'user_id',
        'post_id',
        'content_type',
        'content',
        'is_external',
        'rank_score',
        'date',
        'current_vote'
    )
    
    def __init__(self, entry=None):
        super().__init__(entry)
    
    def generate_context(self):
        return {
            'id':       self.id,
            'user':     User(self.user_id).username,
            'user_id':  self.user_id,
            'date':     self.date,
            'vote':     self.current_vote,
            'content':  self.content_html,
        }
    
    @classmethod
    def get_user_total_comments(cls,user_id):             
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE user_id = %s', (user_id, ))
                list_of_comments = []
                for comment_tuple in cursor.fetchall():
                    list_of_comments.append(Comment(comment_tuple))
                return list_of_comments



