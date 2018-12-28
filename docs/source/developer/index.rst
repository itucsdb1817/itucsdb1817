Developer Guide
===============

Database Design
---------------

We have six main tables as Users, Posts, Comments, Tags, Reports, Votes and one extra table Tag_Moderators. 


Accio project constructed around three main folders such as models, routes and templates.
``models`` includes our main six tables and one extra table as classes. Before starting to build these classes we created a ``BaseModel`` that we can get use of for all of our tables.

So, ``models`` are partial representations of a row in table. 
With the ``BaseModel`` they can be easily retrofitted to use their related tables and implement specific functionality for that table. Much of the
database interfacing happens through these ``models``.
``routes`` are functions that dictate what happens, where. They are invoked when a certain route such as /post/<post_id> is accessed. They retrieve the relevant model and template, render it and send to the user.

``templates`` are pages that are filled with content and sent to the user to interact with.

Additionaly, ``static`` folder includes CSS templated for user interface. We used `Bulma CSS framework <https://dansup.github.io/bulma-templates/>`_ for our project.

.. figure:: images/diagram.png

	E/R Diagram

Code (Model-View-Template Structure)
------------------------------------

Our project utilizes MVT paradigm.

Models
^^^^^^

Models are located in the folder `models/` and they are the main method of how we
interact with out database, representations of our data in the codebase. It is not a full-fledged ORM, but simple changes can be
done and saved without using SQL in views.
Classes that have the parent ``BaseModel`` can be created with creating the following class variables:

* ``TABLE_NAME`` A string that matches the table name in the db
* ``COLUMN_NAMES`` Tuple consisting of strings that matches the column names in the table, in order.

An empty initialization of the child class object results in a new entry in the table upon calling ``.save()``.
Initialization with the entry id results in update of changes of the related entry upon ``.save()``.
It can also initialized with a tuple, which updates the related entry upon ``.save()``. The system assumes it is ordered correctly and matches the
table format, and should be used with caution. It is meant for developers to overload ``__init__()`` and
create their own initalization methods. (*e.g*. Retreiving a user entry by its username).

Code for the ``BaseModel`` class is located at ``models/base.py``

Views
^^^^^

Views are what end-users are exposed to. It couples models and templates, renders them and serves them
to the users.

They are located at the folder ``routes/``

Templates
^^^^^

Templates are not changed significantly and are written in Jinja2 format.

They are located at the folder ``templates/`` and are to be used by views.

.. toctree::

   member1
   member2
