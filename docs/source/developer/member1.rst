Parts Implemented by Buse Kuz
================================

**Tables**
**********

Users
-----

1- Table Creation
~~~~~~~~~~~~~~~~~~

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

* ``id`` ``PRIMARY KEY```
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
~~~~~~~~~~~~~~~~~~


A regular user must be able to register, login, logout, change their password view their profile.
An admin user addtionaly can review reports and update user's attributes and delete them if necessary.
All of those operations are handled in ``user_routes.py``.

**Registration**

User has to register to be a member of Accio community.

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



* Save function uses insert into query to create a User tuple (details of initializations are at BaseModel section).
* ``logged_in`` function checks if there is a user in the session and returns user if there is any
* Flask-bcrypt library is used to store the password hashed in the database which is a much safer approach
* Flask-WTF is used for all forms in the project 



**Login**


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



