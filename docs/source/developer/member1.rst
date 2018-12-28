Parts Implemented by Buse Kuz
================================

**Tables**
**********

Users
-----

This table holds records of registered users. ``Users`` is the main table for the project. The attribute ``id`` is foreign key in 5 other tables.

So ``Users`` has 10 attributes and it is highly connected with the rest of the tables.

Attributes 
^^^^^^^^^^

* ``id``
    - ``PRIMARY KEY``
    - ``SERIAL``
* ``first_name``
    - ``VARCHAR(32)``
    - First name of the user
* ``last_name``
    - ``VARCHAR(32)``
    - Last name of the user
* ``username``
    - ``VARCHAR(32)``
    - Username for user
* ``password``
    - ``VARCHAR(200)``
    - Password of the user
* ``email``
    - ``VARCHAR(254)``
    - E-mail address of user
* ``birth_date``
    - ``DATE``
    - Birth date of user 
* ``date```
    - ``DATE``
    - Date of user's registration
* ``is_admin``
    - ``BOOL``
    - User type
* ``is_banned``
    - ``BOOL``
    - Holds the information of user's ban status

 User has to register to be a member of Accio community. Flask-WTF is used for registration and also at login, submit post etc. 

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

   * Save function uses insert into query to create a User tuple.
   * ``logged_in`` function checks if there is a user in the session and returns user if there is any
   * Flask-bcrypt library is used to store the password hashed in the database which is a much safer approach

