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
    - Primary key of the Users
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
