from flask import current_app
import psycopg2 as db
from models.base import BaseModel
from models.post import Post
from models.user import User
from math import ceil
from datetime import datetime

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
        # tag title
        if isinstance(identifier, str):
            with db.connect(current_app.config['DB_URL']) as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"SELECT * FROM {self.TABLE_NAME} WHERE title=%s",
                    (identifier,)
                )
                t = cursor.fetchone()
                if t is not None:
                    super().__init__(t)
                else:
                    raise NotImplementedError('no tag')
        # tag id or none or direct tuple
        else:
            super().__init__(identifier)

    @classmethod
    def get_all(cls): 
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} LIMIT 5')
                list_of_tags = []
                for tag_tuple in cursor.fetchall():
                    list_of_tags.append(Tag(tag_tuple))
                return list_of_tags
    
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
                pagination = {}
                pagination['page_number'] = 1
                pagination['last_page_number'] = 1
                pagination['posts'] = []  
                return pagination
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

    def mod_add_user(self, user_id):
        if not TagModerator.is_mod(user_id, self.id):
            tm = TagModerator()
            tm.date = datetime.now()
            tm.user_id = user_id
            tm.tag_id = self.id
            tm.save()

    # invoker should be a mod too
    def mod_remove_user(self, user_id):
        TagModerator.delete_rel(user_id, self.id)

    def list_mods(self):
        return TagModerator.list_mods(self.id)



class TagModerator(BaseModel):
    TABLE_NAME = 'tag_moderators'
    COLUMN_NAMES = (
        'id',
        'date',
        'user_id',
        'tag_id'
    )

    @classmethod
    def is_mod(cls, user, tag):
        """
        Checks if the user is a mod in the specified tag
        """
        u = User.TABLE_NAME
        t = Tag.TABLE_NAME
        m = cls.TABLE_NAME

        user_statement = u
        if isinstance(user, str):
            user_statement += '.username'
        elif isinstance(user, int):
            user_statement += '.id'
        else:
            raise TypeError('User parameter must be the username or the id')
        user_statement += '=%s'

        tag_statement = t
        if isinstance(tag, str):
            tag_statement += '.title'
        elif isinstance(tag, int):
            tag_statement += '.id'
        else:
            raise TypeError('Tag parameter must be the tag title or the id')
        tag_statement += '=%s'

        query = (
            f"SELECT {u}.id, {u}.username, {t}.id, {t}.title FROM {m} "
            f"INNER JOIN {u} ON {m}.user_id={u}.id "
            f"INNER JOIN {t} ON {m}.tag_id={t}.id "
            f"WHERE {user_statement} AND {tag_statement}"
        )

        with db.connect(current_app.config['DB_URL']) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user, tag))
            result = cursor.fetchone()
            cursor.close()
            return bool(result)
    
    @classmethod
    def list_mods(cls, tag_id):
        u = User.TABLE_NAME
        m = cls.TABLE_NAME
        query = (
            f"SELECT {u}.id, {u}.username FROM {m} "
            f"INNER JOIN {u} ON {m}.user_id={u}.id "
            f"WHERE {m}.tag_id=%s "
        )
        with db.connect(current_app.config['DB_URL']) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (tag_id, ))
            result = cursor.fetchall()
            return(result)

    @classmethod
    def delete_rel(cls, user_id, tag_id):
        if (not isinstance(user_id, int)) or (not isinstance(tag_id, int)):
            raise NotImplementedError('Must be ids')
        query = f"DELETE FROM {cls.TABLE_NAME} WHERE user_id=%s AND tag_id=%s"
        with db.connect(current_app.config['DB_URL']) as conn:
            cursor = conn.cursor()
            cursor.execute(query, (user_id, tag_id))
            conn.commit()
            cursor.close()
