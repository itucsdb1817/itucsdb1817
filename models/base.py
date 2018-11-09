from typing import Tuple
from flask import current_app
import psycopg2 as db 

# in a created model, following values should be set:
# self._TABLE_NAME, name of the table
# self._COLUMN_NAMES, a tuple consisting of the column names,
# COLUMN NAMES must be the in the same order as they are defined in table

class BaseModel():
    # If an id is given , object tries to find it and copies all values
    # The id attribute of an entry created via id should not be changed
    # After creation all values in database can be
    # accessed and changed with object_name.attribute_name
    # Save method will update the entry in database directly
    # Changing id directly after init should not allowed
    # The existance of _ORIGINAL_ATTR means the object was created
    # from a row in the table
    def __init__(self, entry: int):
        if type(entry) is int:
            assert entry > 0, 'id must be bigger than 0'
            fetched_values = self._from_table_get_by_id(entry_id)
            if not fetched_values:
                raise NotImplementedError(f'Entry with id {entry} was not found in table {self._TABLE_NAME}')
        else if type(entry) is tuple:
            assert len(entry) == len(self.__class__.entry)
            fetched_values = entry
        else:
            raise NotImplementedError('__init__ of base, program shouldnt be here')
        self._ORIGINAL_ATTR = fetched_values
        self._set_attr(fetched_values)
    
    # If an id is not given, an empty entry will be created
    # _ORIGINAL_ATTR will not exist and save function will act accordingly
    # Interface user is expected 
    def __init__(self):
        pass

    # Saves the object to table
    def save(self):
        cursor = self._DATABASE_CONNECTION.cursor()
        if hasattr(self, '_ORIGINAL_ATTR'):
            assert hasattr(self, 'id')
            changed = self._get_changed()
            placeholders = ', '.join((key + ' = %s') for key in changed.keys())
            query = f'''UPDATE {self.__class__.TABLE_NAME}
                        SET {placeholders}
                        WHERE id = {self._ORIGINAL_ATTR[0]}'''
            cursor.execute(query, changed.values())
        else:
            if not self._is_attr_complete():
                raise NotImplementedError('INSUFFICENT ATTR')
            columns = ', '.join(self.__class__.COLUMN_NAMES[1:])
            placeholders = (len(self.__class__.COLUMN_NAMES[1:]) * '%s, ')[:-2]
            query = f'''INSERT INTO {self.__class__.TABLE_NAME} ({columns})
                        VALUES ({placeholders})'''
            cursor.execute(query, self._get_attr[1:])
        cursor.commit()
        cursor.close()
    
    # assign the given elements from the tuple as attributes to the object
    # this method should not be called from outside as input tuple contains id from SQL Query
    def _set_attr(self, t: Tuple):
        for column, value in zip(self.__class__.COLUMN_NAMES, t):
            setattr(self, column, value)
    
    # returns current attributes combined in a tuple
    # (47, 'James', True, ...) etc
    def _get_attr(self):
        return tuple([getattr(self,column) for column in self.__class__.COLUMN_NAMES])
    
    # returns current attributes in a dict with the column names as keys
    # {'id': 47, 'first_name': 'James', 'is_admin': True}
    def _get_attr_dict(self):
        return dict(zip(self.__class__.COLUMN_NAMES, self._get_attr()))

    # send query to find if id exists in the current 
    # if it exists, return as tuple
    def _from_table_get_by_id(self, entry_id: int):
            cursor = self._DATABASE_CONNECTION.cursor()
            cursor.execute(
                f'''SELECT * FROM {self.__class__.TABLE_NAME}
                        WHERE id=%s''',
                (entry_id, )
                )
            return cursor.fetchone()

    # only returns new versions of attributes that have been changed as dictionary
    # must not be called if entity is new
    def _get_changed(self):
        changed = {}
        for column, original, current in zip(self.__class__.COLUMN_NAMES, self._ORIGINAL_ATTR, self._get_attr()):
            if original != current:
                changed[column] = current
        # id should not have been changed
        if 'id' in changed:
            del changed['id']
        return changed

    # if there are any unentered attributes
    def _is_attr_complete(self):
        for column in self.__class__.COLUMN_NAMES[1:]:
            if not hasattr(self, column):
                return False
        return True
    
    @classmethod
    def query_select_all(cls):
        with db.connect(current_app.config['db']) as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT * FROM {cls.TABLE_NAME}')
                return cursor.fetchall()