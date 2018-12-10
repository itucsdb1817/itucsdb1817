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


vote_page = Blueprint('vote_page', __name__,)


@vote_page.route('/vote/<int:parent_id>/<int:vote_type>/<int:parent_type>', methods = ['GET', 'POST'])
def vote_post(parent_id,vote_type,parent_type):
	if check.logged_in():
		if (parent_type == 0 or parent_type == 1) and (vote_type == 0 or vote_type == 1):
			## parent type = 0 post
			## parent type = 1 comment
			create_vote = False
			delete_vote = False
			try:
				if parent_type == 0:
					parent = Post(parent_id)
					user_vote = Vote.get_user_post_vote(session.get("user_id", ""),parent_id)
					if not user_vote:	##User did not vote before
						if(vote_type == 1):
							parent.current_vote += 1
						else:
							parent.current_vote -= 1 
						parent.save()
						create_vote = True
					else:
						if user_vote[0].vote:
							if vote_type == 0:
								parent.current_vote -= 2
							else:
								parent.current_vote -= 1
								delete_vote = True
						else:
							if vote_type == 0:
								parent.current_vote += 1
								delete_vote = True
							else:
								parent.current_vote += 2
						if delete_vote:
							user_vote[0].delete()
						else:
							user_vote[0].vote = bool(vote_type)
							user_vote[0].save()
						parent.save()
				elif parent_type == 1:
					parent = Comment(parent_id)
				if create_vote:
					vote = Vote()
					vote.date = datetime.utcnow()
					vote.parent_type = bool(parent_type)
					vote.passed_time = '1'
					vote.vote = bool(vote_type)
					vote.user_id = session.get("user_id", "")
					vote.post_id = parent_id if parent_type == 0 else None
					vote.comment_id = parent_id if parent_type == 1 else None 
					vote.save()
				return jsonify({'success': 'Successfuly voted!', 'final_vote': parent.current_vote})
			except NotImplementedError as error:
				return jsonify({'error': str(error)})
	return jsonify({'error': 'Invalid vote.'})





















