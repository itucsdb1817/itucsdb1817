from flask import Blueprint, render_template,request, jsonify, session, redirect, flash,current_app
from flask_bcrypt  import Bcrypt
from flask import jsonify

import os
import sys
from datetime import datetime
sys.path.append("../..") # Adds higher directory to python modules path.
from utils import logged_in as check
from models.user import User 
from models.post import Post 
from models.vote import Vote
from models.report import Report
from routes.report.forms import ReportForm



report_page = Blueprint('report_page', __name__,)

##User side of report page
@report_page.route('/report/<int:is_comment>/<int:reported_id>', methods = ['GET', 'POST'])
def report_post(is_comment,reported_id):
	create_report = False
	if not check.logged_in():
		return redirect("/user/login/")
	else:
		form = ReportForm(request.form)
		if form.validate_on_submit():
			try:
				#If reported object is a post
				if is_comment == 0:
					reported_post = Post(reported_id)
					if len(Report.get_user_prev_report(session.get("user_id", ""),reported_id)) > 0:
						return redirect("/post/" + str(reported_id))
				else:
					reported_comment = Comment(reported_id)
					#if len(report.get_user_prev_report(session.get("user_id", ""),reported_id)) > 0:
					#	return redirect("/post/" + reported_id)

				report = Report()
				report.submitting_user_id = session.get("user_id", "")
				report.violated_rule = form.data["violated_rule"]
				report.date = datetime.utcnow()
				report.reason_description = form.data["reason_description"]
				report.is_comment = is_comment
				report.action_taken = None
				report.is_dismissed = False
				report.post_id = reported_id if is_comment == 0 else None
				report.comment_id = reported_id if is_comment == 1 else None
				report.save()
				return redirect("/user/reports")
			except NotImplementedError as error:
				return render_template("error.html", error_type = "Failed", error_info = str(error))
		else:
			if request.method == "POST":
				return render_template('report.html', form=form, error = "Invalid field, please check again.")
			else:
				return render_template('report.html', form=form)




