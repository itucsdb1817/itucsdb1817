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
    - *Type:* ``SERIAL``
    - *Explanation:* Primary key of the Users
* ``first_name``
    - *Type:* ``VARCHAR(32)``
    - *Explanation:* First name of the user
    - *Nullable:* ``NOT NULL``
* ``last_name```
    - *Type:* ``VARCHAR(32)``
    - *Explanation:* Last name of the user
    - *Nullable:* `NOT NULL``
* ``username``
    - *Type:* ``VARCHAR(32)``
    - *Explanation:* Username for user
    - *Nullable:* ``NOT NULL``
* ``password``
    - *Type:* ``VARCHAR(200)``
    - *Explanation:* Password of the user
    - *Nullable:* ``NOT NULL``
* ``email``
    - *Type:* ``VARCHAR(254)``
    - *Explanation:* E-mail address of user
* ``birth_date``
    - *Type:* ``DATE``
    - *Explanation:* Birth date of user 
* ``date```
    - *Type:* ``DATE``
    - *Explanation:* Date of user's registration
* ``is_admin``
    - *Type:* ``BOOL``
    - *Explanation:* User type
* ``is_banned``
    - *Type:* ``BOOL``
    - *Explanation:* Holds the information of user's ban status
