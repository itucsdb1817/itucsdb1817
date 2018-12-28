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

* :sql:`id`
    - :sql:`PRIMARY KEY`
    - *Type:* :sql:`SERIAL`
    - *Explanation:* Primary key of the Users
* :sql:`first_name`
    - *Type:* :sql:`VARCHAR(32)`
    - *Explanation:* First name of the user
    - *Nullable:* :sql:`NOT NULL`
* :sql:`last_name`
    - *Type:* :sql:`VARCHAR(32)`
    - *Explanation:* Last name of the user
    - *Nullable:* :sql:`NOT NULL`
* :sql:`username`
    - *Type:* :sql:`VARCHAR(32)`
    - *Explanation:* Username for user
    - *Nullable:* :sql:`NOT NULL`
* :sql:`password`
    - *Type:* :sql:`VARCHAR(200)`
    - *Explanation:* Password of the user
    - *Nullable:* :sql:`NOT NULL`
* :sql:`email`
    - *Type:* :sql:`VARCHAR(254)`
    - *Explanation:* E-mail address of user
* :sql:`birth_date`
    - *Type:* :sql:`DATE`
    - *Explanation:* Birth date of user 
* :sql:`date`
    - *Type:* :sql:`DATE`
    - *Explanation:* Date of user's registration
* :sql:`is_admin`
    - *Type:* :sql:`BOOL`
    - *Explanation:* User type
* :sql:`is_banned`
    - *Type:* :sql:`BOOL`
    - *Explanation:* Holds the information of user's ban status
