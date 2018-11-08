from typing import Tuple
from flask import current_app
import psycopg2 as db 

# in a created model, following values should be set:
# self._TABLE_NAME, name of the table
# self._COLUMN_NAMES, a tuple consisting of the column names,
# COLUMN NAMES must be the in the same order as they are defined in table

class BaseModel():

    def __init__(self, entry, iterable_has_id=False):
        # If an id is given , object tries to find it and copies all values
        # The id attribute of an entry created via id should not be changed
        # After creation all values in database can be
        # accessed and changed with object_name.attribute_name
        # Save method will update the entry in database directly
        # Changing id directly after init is not allowed
        if type(entry) is int:
            if entry < 1:
                raise IndexError('id of an table entry cannot be less than zero')
            fetched_values = self._from_table_get_by_id(entry_id)
            if not fetched_values:
                raise NotImplementedError(f'Entry with id {entry} was not found in table {self._TABLE_NAME}')
            else:
                # The existance of _ORIGINAL_ATTR means the object was created
                # from an row in the table
                # All changes will effect that row
                self._ORIGINAL_ATTR = fetched_values
                self._set_attr(fetched_values)

        # Creation with a tuple or a dict results in a brand new entry candidate
        # It is recommended that the passed in container does not contain id
        # If the container has an id, because it is a new entry, it will be discarded
        if type(entry) is tuple:
            if iterable_has_id and (len(entry) != len(self._COLUMN_NAMES)):
                throw NotImplementedError()
            if not iterable_has_id and (len(entry) != (len(self._COLUMN_NAMES) - 1)):
                throw NotImplementedError()
            

        else:
            pass
    
    # assign the given elements from the tuple as attributes to the object
    # this method should not be called from outside as input tuple contains id from SQL Query
    def _set_attr(self, t: Tuple):
        for column, value in zip(self._COLUMN_NAMES, t):
            setattr(self, column, value)
    
    # returns current attributes combined in a tuple
    # (47, 'James', True, ...) etc
    def _get_attr(self):
        return tuple([getattr(self,column) for column in self._COLUMN_NAMES])
    
    # returns current attributes in a dict with the column names as keys
    # {'id': 47, 'first_name': 'James', 'is_admin': True}
    def _get_attr_dict(self):
        return dict(zip(self._COLUMN_NAMES, self._get_attr_tuple()))

    # send query to find if id exists in the current 
    def _from_table_get_by_id(self, entry_id: int):
            cursor = self._DATABASE_CONNECTION.cursor()
            cursor.execute(
                f'''SELECT * FROM {self._TABLE_NAME}
                        WHERE id=%s''',
                (entry_id, )
                )
            return cursor.fetchone()

    # only returns new versions of attributes that have been changed as dictionary
    def _get_changed(self):
        changed = {}
        if not hasattr(self, '_ORIGINAL_ATTR'):
            return changed
        for column, original, current in zip(self._COLUMN_NAMES, self._ORIGINAL_ATTR, self._get_attr()):
            if original != current:
                changed[column] = current
        return changed

        
    # Query that list specified columns in referenced table,
    def _from_table_select(self, column_names: Tuple[str]): 
        flattened_columns = ', '.join(column for column in columns)
        with current_app.config['db'].cursor() as cursor:
            cursor.execute(f'SELECT {flattened_columns} FROM {self._TABLE_NAME}')
            return cursor.fetchall()

    # Query that list specified columns in referenced table,
    def _from_table_select_all(self) -> Tuple[str]:
        with current_app.config['db'].cursor() as cursor:
            cursor.execute(f'SELECT * FROM {self._TABLE_NAME}')
            return cursor.fetchall()
