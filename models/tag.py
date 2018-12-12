from flask import current_app
import psycopg2 as db
from models.base import BaseModel
from models.post import Post
from models.user import User
from math import ceil

class Tag(BaseModel):
    TABLE_NAME = 'tags'
    COLUMN_NAMES = (
        'id',
        'title',
        'date',
        'subscriber_amount',
        'is_banned',
        'description',
        'rules'
    )

    def __init__(self, identifier=None):
        # tag id
        if isinstance(identifier, int):
            super().__init__(identifier)
        # tag title
        elif isinstance(identifier, str):
            with db.connect(current_app.config['DB_URL']) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"SELECT * FROM {self.TABLE_NAME} WHERE title=%s",
                    (identifier,)
                )
                t = cursor.fetchone()
                if t is not None:
                    super().__init__(t)
                    return
                else:
                    raise NotImplementedError('no tag')
    
    def paginate(self, page, page_size=20):
        """
        This method paginates the entries in database.
        """
        assert page > 0
        with db.connect(current_app.config['DB_URL']) as conn:
            # TODO: Selection of sorting
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(id) FROM posts WHERE tag_id={self.id}")
            count = cursor.fetchone()[0]
            if count == 0:
                # table is empty, abort
                return None
            # Normalize page index if it exceeds max page count
            pagination = {}
            max_page_count = int(ceil(count / page_size))
            if max_page_count < page:
                page = max_page_count
            pagination['page_number'] = page
            pagination['last_page_number'] = max_page_count
            pagination['posts'] = []
            cursor.execute(f"SELECT * FROM posts WHERE tag_id={self.id}")
            for i in range(page):
                post_tuples = cursor.fetchmany(page_size)
                if post_tuples is None:
                    raise IndexError('No set of posts left to render')
            for post_tuple in post_tuples:
                post = Post(post_tuple)
                info = {
                    'title':    post.title,
                    'id':       post.id,
                    'user':     User(post.user_id).username,
                    'vote':     post.current_vote,
                    'date':     post.date
                }
                pagination['posts'].append(info)
            cursor.close()
            return pagination


class TagSubscription(BaseModel):
    TABLE_NAME = 'tag_susbcriptions'
    COLUMN_NAMES = (
        'id',
        'date',
        'user_id',
        'tag_id'
    )

    def __init__(self, entry_id=-1):
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
        if entry_id != -1:
            super().__init__(entry_id)