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

 .. literalinclude:: /../../routes/user/user_routes.py
   :language: python
   :linenos:
   :caption: **Registration** (file: ``routes/user/user_routes.py``)
   :name: Register Route
   :lines: 62-99

   * Save function uses insert into query to create a User tuple.
   * ``logged_in`` function checks if there is a user in the session and returns user if there is any

