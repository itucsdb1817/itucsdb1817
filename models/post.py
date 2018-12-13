from typing import Tuple
from flask import current_app
import psycopg2 as db 
from models.base import BaseModel
from models.user import User
from models.comment import Comment


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
        'tag_id',
        'date',
        'title',
        'content_type',
        'content',
        'is_external',
        'current_vote',
        'rank_score',
        'is_banned',
        'comment_count'
    )
    def __init__(self, entry_id=None, get_comments=False):
        super().__init__(entry_id)
        if hasattr(self, '_ORIGINAL_ATTR') and get_comments:
            self._get_comments()

    ## NEW FUNCTIONS HERE
    # RULE OF THUMB:
    #       IF YOU NEED TO ACCESS COLUMN VALUES, USE NORMAL METHODS
    
    def _get_comments(self):
        """
        This method will retreive all parent comments with each
        parent comment containing their children comments
        """
        if not hasattr(self, '_ORIGINAL_ATTR'):
            raise NotImplementedError('This method cannot be called on a fresh entry')
        self._comments = []
        with db.connect(current_app.config['DB_URL']) as conn:
            cursor = conn.cursor()
            # only retreive parent comments
            query = f"SELECT * FROM {Comment.TABLE_NAME} WHERE parent_id IS NULL AND post_id=%s"
            cursor.execute(query, (self.id, ))
            results = cursor.fetchall()
            cursor.close()

        for result in results:
            self._comments.append(Comment(result, get_children=True))

    def _generate_context_meta(self):
        return {
            'user':     User(self.user_id).username,
            'user_id':  self.user_id,
            'date':     self.date,
            'vote':     self.current_vote,
            'comment':  self.comment_count
        }

    def _generate_context_post(self):
        return {
            # TODO: Carry id to meta
            'id':       self.id,
            'title':    self.title,
            'body':     self.content
        }
     
    def _generate_context_comments(self):
        comment_array = []
        if not hasattr(self, '_comments'):
            return comment_array
        for comment in self._comments:
            comment_array.append(comment.generate_context())
        return comment_array

    def generate_context(self):
        """
        This method generates the context that will be used to render
        the post template.
        """
        context = {}
        context['meta'] = self._generate_context_meta()
        context['post'] = self._generate_context_post()
        context['comments'] = self._generate_context_comments()
        return context

        

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
