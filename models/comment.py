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
        'parent_id',
        'content_type',
        'content',
        'is_external',
        'rank_score',
        'date',
        'current_vote'
    )
    
    def __init__(self, entry=None, get_children=False):
        """
        Get comments with or without children
        """
        self._children = []
        if entry is None:
            get_children = False

        super().__init__(entry)

        if get_children:
            self._get_children()

    
    def _get_children(self):
        """
        Get all comments that reply to this comment.

        This method will get all children below itself.
        """
        with db.connect(current_app.config['DB_URL']) as conn:
            cursor = conn.cursor()
            query = f"SELECT * FROM {self.__class__.TABLE_NAME} WHERE parent_id IS NOT NULL AND parent_id=%s"
            cursor.execute(query, (self.id, ))
            results = cursor.fetchall()
            cursor.close()

        # calling this recursively with get_children=True
        # would create overhead not recommended
        for result in results:
            self._children.append(Comment(result))

        for child in self._children:
            child._get_children()

    def _generate_context_comment(self):
        return {
            'id':       self.id,
            'user':     User(self.user_id).username,
            'user_id':  self.user_id,
            'date':     self.date,
            'vote':     self.current_vote,
            'content':  self.content,
            'children': []
        }
    
    def generate_context(self):
        """
        Recursively generates the context needed for displaying the comments
        """
        context = self._generate_context_comment()
        if hasattr(self, '_children'):
            for child in self._children:
                context['children'].append(child.generate_context())
        return context

    @classmethod
    def get_user_total_comments(cls,user_id):             
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE user_id = %s', (user_id, ))
                list_of_comments = []
                for comment_tuple in cursor.fetchall():
                    list_of_comments.append(Comment(comment_tuple))
                return list_of_comments



