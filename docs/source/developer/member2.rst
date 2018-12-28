Parts Implemented by Efe Hakan Gençoğlu
================================

**Tags**

1 - Table Creation
~~~~~~~~~~~~~~~~~~

This table provides common tags for posts to be submitted under.
All posts must be submitted with a tag.
It does not reference any other tables.

.. code-block:: sql

        CREATE TABLE tags (
            id serial  NOT NULL,
            title text  NOT NULL,
            date timestamp  NOT NULL,
            subscriber_amount int  NOT NULL,
            is_banned boolean  NOT NULL,
            description text  NULL,
            rules text  NULL,
            CONSTRAINT tags_pk PRIMARY KEY (id)
        );


* ``id`` ``PRIMARY KEY``
* ``title`` Title of the tag.
* ``date`` Creation date of the tag.
* ``subscriber_amount`` Amount of people who subscribed to this tag.
* ``is_banned`` Whether the tag has been banned or not.
* ``description`` A short description of this tag/community.
* ``rules`` Rules that are decided by the moderators of the tag.

2 - Tag Routes
~~~~~~~~~~~~~~~

All viewers can view a tag, but only tag creators and moderators selected
by the tag creator and the other mods are allowed to access the
moderation page.

**Tag Creation**

User must be logged in to create a tag.
