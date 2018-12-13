from typing import Tuple
from flask import current_app
import psycopg2 as db 
from models.base import BaseModel



class Report(BaseModel):
    TABLE_NAME = 'reports'
    COLUMN_NAMES = (
        'id', 
        'submitting_user_id',
        'violated_rule',
        'date',  
        'reason_description',
        'is_comment',
        'action_taken',
        'is_dismissed', 
        'post_id',
        'comment_id'
    )
    def __init__(self, entry_id=None):
        super().__init__(entry_id)


    @classmethod
    def get_user_prev_report(cls,user_id,post_id):             
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE submitting_user_id = %s AND post_id = %s', (user_id,post_id, ))
                list_of_reports = []
                for report_tuple in cursor.fetchall():
                    list_of_reports.append(Report(report_tuple))
                return list_of_reports

    @classmethod
    def get_user_all_reports(cls,user_id):             
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE submitting_user_id = %s', (user_id, ))
                list_of_reports = []
                for report_tuple in cursor.fetchall():
                    list_of_reports.append(Report(report_tuple))
                return list_of_reports


    


    def delete(self):
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'DELETE FROM {self.TABLE_NAME} WHERE id= %s', (self.id, ))
                
