from flask import current_app
from models.base import BaseModel
import psycopg2 as db

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

        super.__init__(entry)

        if get_children:
            self._get_children()

    
    def _get_children(self):
        """
        Get all comments that reply to this comment.

        This method will get all children below itself.
        """
        with db.connect(current_app.config['DB_URL']) as conn:
            cursor = conn.cursor()
            query = "SELECT * FROM comments WHERE parent_id IS NOT NULL AND parent_id=%s"
            cursor.execute(query, (self.id, ))
            results = cursor.fetchall()
            cursor.close()

        # calling this recursively with get_children=True
        # would create overhead not recommended
        for result in results:
            self._children.append(Comment(result))

        for child in self._children:
            child._get_children()
