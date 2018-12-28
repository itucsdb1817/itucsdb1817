Parts Implemented by Buse Kuz
================================

**Users**
*********

1- Table Creation
~~~~~~~~~~~~~~~~

This table holds records of registered users. ``Users`` is the main table for the project. The attribute ``id`` is foreign key in 5 other tables.

So ``Users`` has 10 attributes and it is highly connected with the rest of the tables.


.. code-block:: sql

	    CREATE TABLE users (
	        id serial  NOT NULL,
	        first_name varchar(32)  NOT NULL,
	        last_name varchar(32)  NOT NULL,
	        username varchar(32)  NOT NULL,
	        password varchar(200)  NOT NULL,
	        email varchar(254)  NOT NULL,
	        birth_date date  NOT NULL,
	        is_admin boolean  NOT NULL,
	        is_banned boolean  NOT NULL,
	        date timestamp  NOT NULL,
	        CONSTRAINT id PRIMARY KEY (id)
	    );

* ``id`` ``PRIMARY KEY``
* ``first_name``	First name of the user
* ``last_name``	Last name of the user
* ``username``	Username for user
* ``password``	Password of the user
* ``email``	E-mail address of user
* ``birth_date``	Birth date of user 
* ``date``	Date of user's registration
* ``is_admin``	User type
* ``is_banned``	Holds the information of user's ban status


2- User Routes
~~~~~~~~~~~~~~~~




A regular user must be able to register, login, logout, change their password view their profile.
An admin user addtionaly can review reports and update user's attributes and delete them if necessary.
All of those operations are handled in ``user_routes.py``.

* Flask-WTF is used for all forms at the routes.
* `Flask-Bcrypt <https://flask-bcrypt.readthedocs.io/en/latest/>`_ library is used to store the password hashed in the database which is a much safer approach



**Registration**

.. code-block:: python

		@user_page.route('/user/register', methods = ['GET', 'POST'])
		def register():
		    if check.logged_in():
		        return redirect("/") 
		    else:
		        form = RegistrationForm(request.form)		
		        if form.validate() == False:
		            print(form.errors) 

		        if form.validate_on_submit():
		            username = form.data["username"]
		            email = form.data["email"]
		            unique_check = User.unique_user_check(username,email)

		            if unique_check:
		                new_user = User()
		                new_user.first_name = form.data["firstname"]
		                new_user.last_name = form.data["lastname"]
		                new_user.username = form.data["username"]
		                new_user.birth_date = form.data["birth_date"]
		                new_user.email = form.data["email"]
		                password_hash = current_app.config['bcrypt'].generate_password_hash(form.data["password"]).decode('utf-8')
		                new_user.password = password_hash
		                new_user.is_admin = False
		                new_user.is_banned = False
		                new_user.date = datetime.utcnow()
		                new_user.save()
		                flash({'text': "You have successfully signed up!", 'type': "success"}) 
		                return redirect("/")
		            else:
		                return render_template('register.html', form=form, error = "This username or e-mail is already in use, please try another one.")
		        else:
		            if request.method == "POST":
		                return render_template('register.html', form=form, error = ", field, please check again.")
		            else:
		                return render_template('register.html', form=form)
		    return render_template('register.html', form=form)



* ``user.save()`` function uses "INSERT" query from base.py to create a User tuple (details of initializations are at BaseModel section).
* ``logged_in`` function checks if there is a user in the session and returns user if it exists.



**Login**

Users can login with their username and password unless they are banned.


.. code-block:: python
		
		@user_page.route('/user/login', methods = ['GET', 'POST'])
		def login():
		    if check.logged_in():
		        return redirect("/") 
		    form = LoginForm()
		    if form.validate_on_submit():
		        username = form.data["username"]
		        user = User.get_from_username(username)	

		        if user is not None:
		            if user.is_banned is True:
		                flash({'text': "You are banned from Accio, you can not sign in.", 'type': "error"}) 
		                return redirect("/")
		            password = form.data["password"]
		            password_hash = user.password
		            if current_app.config['bcrypt'].check_password_hash(password_hash, password):
		                session['user_id'] = user.id
		                flash({'text': "You have successfully logged in.", 'type': "success"}) 
		                return redirect("/")
		            else:
		                return render_template("login.html", form=form,error = "Incorrect password.")
		        else:
		            return render_template("login.html", form=form,error = "Incorrect username or password.")
		    return render_template("login.html", form=form)

		    @user_page.route('/user/login', methods = ['GET', 'POST'])



**Logout**


.. code-block:: python

		@user_page.route('/user/logout')
		def logout():
		    session.pop("user_id",None)
		    flash({'text': "You have successfully logged out.", 'type': "success"}) 
		    return redirect("/")


.. note:: Flask-Session is an extension for Flask that adds support for Server-side Session to your application. It is essential to know which user is in the session while user is visiting routes. Session is setted in ``login`` and popped at ``logout``.


**Profile**

Anyone can view user profiles except these slight differences,

* If user views their own profile they can edit change their password or delete their reports.

* If logged in user is an admin, admin can ban the user from their profile.

.. code-block:: python

		@user_page.route('/user/profile/<int:id>', methods = ['GET', 'POST'])
		def profile_page(id):
		    try:
		        admin = False
		        ban = False
		        self_profile = False
		        if check.logged_in():
		            if id == session.get("user_id",""):
		                self_profile = True
		        if admin_check.admin_logged_in():
		            admin = True
		        user = User(id)
		        if user.is_banned == True:
		        	ban = True
		       	
		        parent_list = []
		        for vote in Vote.get_user_total_votes(user.id):
		        	if vote.is_comment == 1:
		        		parent_list.append(Comment(vote.comment_id))
		        	elif vote.is_comment == 0:
		        		parent_list.append(Post(vote.post_id))


		        return render_template('profile.html',id=user.id, username = user.username, first_name = user.first_name, last_name = user.last_name, birth_date = user.birth_date, creation_date = user.date, posts = Post.get_user_post(user.id),email= user.email, self_profile = self_profile, total_votes = Vote.get_user_total_votes(user.id), comments = Comment.get_user_total_comments(user.id), reports = Report.get_user_all_reports(user.id), parent_list = parent_list, admin=admin, ban= ban)

		    except NotImplementedError as error:
		        flash("Error: " + str(error))
		        return redirect("/") 




.. code-block:: python

		@user_page.route('/user/change_password', methods = ['GET', 'POST'])
		def change_password():
		    if check.logged_in():
		        form = PasswordForm()
		        if form.validate_on_submit():
		            user = User(session.get("user_id",""))
		            password = form.data["old_password"]
		            password_hash = user.password
		            if current_app.config['bcrypt'].check_password_hash(password_hash, password):
		                user.update_password(current_app.config['bcrypt'].generate_password_hash(form.data["new_password"]).decode('utf-8'))
		                return render_template('change_password.html', form=form, success = "Your password has been updated.")
		            else:
		                return render_template('change_password.html', form=form, error = "Incorrect password.")
		        else:
		            if request.method == "POST":
		                return render_template('change_password.html', form=form, error = "Invalid field, please check again.")
		            else:
		                return render_template('change_password.html', form=form)
		    else:
		        flash({'text': "You have to sign in to change your password.",'type':'is-warning'})
		        return redirect("/user/login")


* This route works at the background and calls ``update_password`` function from ``user.py``.

.. code-block:: python

	    def update_password(self,new_password):
	        with db.connect(current_app.config['DB_URL']) as conn:
	            with conn.cursor() as cursor:
	                cursor.execute(f'UPDATE {self.TABLE_NAME} SET  password = %s WHERE id = %s', (new_password,self.id, ))



3- Methods and Queries
~~~~~~~~~~~~~~~~~~~~~~

* SELECT
	Any user with an id can be accessed by this approach.

.. code-block:: python

		user = User(id)


* UPDATE
	``save()`` function or a specific method such as ``update_password`` from ``user.py`` can be used.

* DELETE
	Admins can delete the user that they view in administration page.
	``delete()`` is imported from base.py

.. code-block:: python

		@admin_user_page.route('/delete_user/<int:id>', methods = ['GET', 'POST'])
		def delete_user(id):
		#Admins can delete the user with given id using this function. 
		    if check.admin_logged_in():   
		        try:
		            user = User(id)
		            user.delete()
		            flash({'text': "This account is deleted permanently.", 'type': 'success'}) 
		            return redirect("/admin/view_users")
		        except NotImplementedError as error:
		            flash({'text': "This account does not exist.", 'type': "Error:" + str(error)}) 
		            return redirect("/")
		    else:
		        flash({'text': "You have to sign in to your admin account first.", 'type': "error"}) 
		        return redirect("/user/login")


Also a few helper methods are implemented at ``user.py`` to fasten some operations.

* ``get_from_username`` is a method that returns User object with requested username.

.. code-block:: python

	    @classmethod
	    def get_from_username(cls, username):
	        with db.connect(current_app.config['DB_URL']) as conn:
	            with conn.cursor() as cursor:
	                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE username = %s', (username, ))
	                if cursor.rowcount == 0:
	                    return None
	                tuple = (cursor.fetchone())
	                u=User(tuple[0])
	                print(u.username)
	                return User(tuple[0])


* ``unique_user_check`` is a method returns true if there is no other user with the same username or email.

.. code-block:: python

	    @classmethod
	    def unique_user_check(cls, username, email):
	        with db.connect(current_app.config['DB_URL']) as conn:
	            with conn.cursor() as cursor:
	                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE email = %s OR username = %s', (email,username, ))
	                if cursor.rowcount == 0:
	                    return True
	                else:
	                    return False    





**Votes**
*********

1- Table Creation
~~~~~~~~~~~~~~~~~~

This table holds records of every vote. 


.. code-block:: sql

		    CREATE TABLE votes (
	        id serial  NOT NULL,
	        user_id int  NOT NULL,
	        date timestamp  NOT NULL,
	        is_comment bool  NOT NULL,
	        vote boolean  NOT NULL,
	        vote_ip varchar(32) NOT NULL,
	        last_update_time timestamp NOT NULL,
	        post_id int  NULL,
	        comment_id int  NULL,
	        CONSTRAINT votes_pk PRIMARY KEY (id)
	    );


* ``id`` ``PRIMARY KEY``
* ``post_id`` ``FOREIGN KEY``
* ``comment_id`` ``FOREIGN KEY``


2- Vote Routes
~~~~~~~~~~~~~~~

* A user can have only one vote per comment or post that is either upvote or downvote.
* There is only one vote route and it works at the background of project.

When a user decides to click on vote several scenarios may occur such as,

* If user had voted this post/comment before,
	-  ``UPDATE`` : User can change his or her vote from upvote to down vote or vice versa.


.. code-block:: python

		
		@vote_page.route('/vote/<int:parent_id>/<int:vote_type>/<int:parent_type>', methods = ['GET', 'POST'])
		def vote_post(parent_id,vote_type,parent_type):
		    if check.logged_in():
		        if (parent_type == 0 or parent_type == 1) and (vote_type == 0 or vote_type == 1):
		            ## parent type = 0 post, parent type = 1 comment
		            create_vote = False
		            delete_vote = False
		            try:
		                if parent_type == 0:
		                    parent = Post(parent_id)
		                    user_vote = Vote.get_user_post_vote(session.get("user_id", ""),parent_id)

		                elif parent_type == 1:
		                    parent = Comment(parent_id)
		                    user_vote = Vote.get_user_comment_vote(session.get("user_id", ""),parent_id)


		                if not user_vote:					#User did not vote this post before
		                    if(vote_type == 1):				#If upvote increment the count, else decrement.
		                        parent.current_vote += 1
		                    else:
		                        parent.current_vote -= 1 
		                    parent.save()
		                    create_vote = True


* If user had voted this post/comment before,
	-  ``DELETE`` : User may want to take his or her vote back.


.. code-block:: python

		else:								#User voted this post before
		    if user_vote[0].vote:			#Previous vote was upvote
		        if vote_type == 0:			#User wants to change the vote to downwote
		            parent.current_vote -= 2
		            user_vote[0].last_update_time = datetime.utcnow()
		            user_vote[0].save()
		        else:
		            parent.current_vote -= 1 #User takes the vote back by clicking twice
		            delete_vote = True		 #Vote will be delete
		    else:							 #Previous vote was downvote
		        if vote_type == 0:			 #Current vote is downvote
		            parent.current_vote += 1 #Vote will be deleted since it was clicked twice
		            delete_vote = True
		        else:
		            parent.current_vote += 2	#User wants to chane the vote to upvote
		            user_vote[0].last_update_time = datetime.utcnow()
		            user_vote[0].save()
		    if delete_vote:
		        user_vote[0].delete()
		    else:
		        user_vote[0].vote = bool(vote_type)
		        user_vote[0].save()
		    parent.save()



* If user is voting for the first time,
	- ``CREATE`` : After we set the attributes of vote object, we save it at the end.


.. code-block:: python		                 
		                
	    #New vote gets created and sended as a JSON object
	    if create_vote:
	        vote = Vote()
	        vote.date = datetime.utcnow()
	        vote.is_comment = bool(parent_type)
	        vote.vote = bool(vote_type)
	        vote.vote_ip = request.remote_addr
	        vote.last_update_time = datetime.utcnow()
	        vote.user_id = session.get("user_id", "")
	        vote.post_id = parent_id if parent_type == 0 else None
	        vote.comment_id = parent_id if parent_type == 1 else None 
	        vote.save()
	    return jsonify({'success': 'Successfuly voted!', 'final_vote': parent.current_vote})
	except NotImplementedError as error:
	    return jsonify({'error': str(error)})
	return jsonify({'error': 'Invalid vote.'})




Also there are a few class methods at ``vote.py`` that will fasten the process. These are mostly need because we need to seperate voted posts and comments from each other to display them to user.

.. code-block:: python

	    @classmethod
	    def get_user_post_vote(cls,user_id,post_id):             
	        with db.connect(current_app.config['DB_URL']) as conn:
	            with conn.cursor() as cursor:
	                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE user_id = %s AND post_id = %s', (user_id,post_id, ))
	                list_of_votes = []
	                for vote_tuple in cursor.fetchall():
	                    list_of_votes.append(Vote(vote_tuple))
	                return list_of_votes

	    @classmethod
	    def get_user_comment_vote(cls,user_id,comment_id):             
	        with db.connect(current_app.config['DB_URL']) as conn:
	            with conn.cursor() as cursor:
	                cursor.execute(f'SELECT * FROM {cls.TABLE_NAME} WHERE user_id = %s AND comment_id = %s', (user_id,comment_id, ))
	                list_of_votes = []
	                for vote_tuple in cursor.fetchall():
	                    list_of_votes.append(Vote(vote_tuple))
	                return list_of_votes



**Reports**
***********


1- Table Creation
~~~~~~~~~~~~~~~~~~

Reports are submitted by users about a specific comment or post.
User has to explain the reason of report, later admins can review these and decide what to do next.

.. code-block:: sql

			CREATE TABLE reports (
	        id serial  NOT NULL,
	        submitting_user_id int  NOT NULL,
	        violated_rule text  NOT NULL,
	        date timestamp  NOT NULL,
	        reason_description text  NOT NULL,
	        is_comment int  NOT NULL,
	        action_taken text  NULL,
	        is_dismissed boolean  NOT NULL,
	        post_id int  NULL,
	        comment_id int  NULL,
	        CONSTRAINT reports_pk PRIMARY KEY (id)
   		);


* ``id`` ``PRIMARY KEY``
* ``post_id`` ``FOREIGN KEY``
* ``comment_id`` ``FOREIGN KEY``


2- Report Routes
~~~~~~~~~~~~~~~~

Report is created same way as other classes.

* ``CREATE`` : It is created when a user first fills the form to report a post/comment.

.. code-block:: python

		 #If reported object is a post
                if is_comment == 0:
                    reported_post = Post(reported_id)
                    if len(Report.get_user_prev_report(session.get("user_id", ""),reported_id)) > 0:
                        return redirect("/post/" + str(reported_id))
                else:
                    reported_comment = Comment(reported_id)
                    if len(Report.get_user_prev_report(session.get("user_id", ""),reported_id)) > 0:
                        return redirect("/post/" + str(reported_comment.post_id))
                    
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


Deletion of the report is only possible by its owner.


* ``DELETE`` : Deletion of the report is only possible by its owner.

.. code-block:: python


		@report_page.route('/report_delete/<int:submitter_id>/<int:id>', methods = ['GET', 'POST'])
		def delete_report(submitter_id,id):
		    if not check.logged_in():
		        flash({'text': "Please sign in.", 'type': "error"}) 
		        return redirect("/") 
		    else:
		        if submitter_id == session.get("user_id",""):
		            report = Report(id)
		            report.delete()
		            flash({'text': "You have deleted a report.", 'type': "success"}) 
		            return redirect("/user/profile/" + str(submitter_id))
		        else:
		            flash({'text': "You can not delete another user's report.", 'type': "error"}) 
		            return redirect("/") 



* ``UPDATE`` : Admins can update a report and saves the action they will take to database.

.. code-block:: python
	

	    def update_for_review(self,action,is_dismissed):
	        with db.connect(current_app.config['DB_URL']) as conn:
	            with conn.cursor() as cursor:
	                cursor.execute(f'UPDATE {self.TABLE_NAME} SET  action_taken = %s , is_dismissed = %s WHERE id = %s', (action,is_dismissed,self.id, ))




