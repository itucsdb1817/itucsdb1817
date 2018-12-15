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

    """
    This function returns a user's list of reports for a specific post
    in order to check if the user reported this post before.
    """
    @classmethod
    def get_user_prev_report(cls,user_id,post_id):             
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE submitting_user_id = %s AND post_id = %s', (user_id,post_id, ))
                list_of_reports = []
                for report_tuple in cursor.fetchall():
                    list_of_reports.append(Report(report_tuple))
                return list_of_reports
                
    """
    This function returns a user's list of reports for a specific comment
    in order to check if the user reported this comment before.
    """
    @classmethod
    def get_user_prev_comment_report(cls,user_id,comment_id):             
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE submitting_user_id = %s AND comment_id = %s', (user_id,comment_id, ))
                list_of_reports = []
                for report_tuple in cursor.fetchall():
                    list_of_reports.append(Report(report_tuple))
                return list_of_reports

    """
    Returns list of reports that submitted by given id.
    Users either can view their reports as a section of their
    profile or directly view the necessary route.
    """
    @classmethod
    def get_user_all_reports(cls,user_id):             
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE submitting_user_id = %s', (user_id, ))
                list_of_reports = []
                for report_tuple in cursor.fetchall():
                    list_of_reports.append(Report(report_tuple))
                return list_of_reports
    """
    Returns all reports that are not reviewed before any admin.
    """
    @classmethod
    def get_reports(cls):             
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE is_dismissed = FALSE')
                list_of_reports = []
                for report_tuple in cursor.fetchall():
                    list_of_reports.append(Report(report_tuple))
                return list_of_reports


    """
    This function updates reports from the admin side, admins are able to update is_dismissed
    and action_taken for each report wtih the given id.
    """
    def update_for_review(self,action,is_dismissed):
        with db.connect(current_app.config['DB_URL']) as conn:
            with conn.cursor() as cursor:
                cursor.execute(f'UPDATE {self.TABLE_NAME} SET  action_taken = %s , is_dismissed = %s WHERE id = %s', (action,is_dismissed,self.id, ))
                

