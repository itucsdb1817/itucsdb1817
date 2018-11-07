from typing import Tuple
from flask import current_app
import psycopg2 as db 

# in a created model, following values should be set:
# self._TABLE_NAME, name of the table
# self._COLUMN_NAMES, a tuple consisting of the column names,
# COLUMN NAMES must be the in the same order as they are defined in table

class BaseModel():
    # assigns
    def __init__(self, entry_id=-1):
        if entry_id > 0:
            fetched_values = self._table_get_by_id(entry_id)
            if not fetched_values:
                # raise some error
                raise NotImplementedError();
            for attr, value in zip(self._COLUMN_NAMES, fetched_values):
                setattr(self, attr, value)
            
    def _table_get_by_id(self, entry_id: int) -> Tuple[str]:
        with current_app.config['db'].cursor() as cursor:
            cursor.execute(
                f'''SELECT * FROM {self._TABLE_NAME}
                        WHERE id=%s''',
                (entry_id, )
                )
            return cursor.fetchone()
        
    # Query that list specified columns in referenced table,
    def _table_list(self, column_names: Tuple[str]): 
        flattened_columns = ', '.join(column for column in columns)
        with current_app.config['db'].cursor() as cursor:
            cursor.execute(f'SELECT {flattened_columns} FROM {self._TABLE_NAME}')
            return cursor.fetchall()

    def _table_list_all(self) -> Tuple[str]:
        with current_app.config['db'].cursor() as cursor:
            cursor.execute(f'SELECT * FROM {self._TABLE_NAME}')
            return cursor.fetchall()