Parts Implemented by Efe Hakan Gençoğlu
================================

Tags
----

Actions:

    - Tag Creation
    - Tag Moderation

Users can create tags through ``/tag_create``.

.. figure:: images/create_tag.png
   :align: center

   Tag Creation

After the tag has been created and filled with posts, the tag
can be viewed from the route ``/t/<tag_title>``

.. figure:: images/tag.png
   :align: center

   Tag View

After this, moderators of the tag can access the moderation page at
``/t/<tag_title>/mod``

.. figure:: images/tag_moderation.png
   :align: center

   Tag Moderation Page

Posts
-----

After a tag has been created, users can submit posts to these tags

Users can submit posts at ``/post/submit``

.. figure:: images/create_post.png
   :align: center

   Post Creation

After the post is created the user is redirected to the post page
at ``/post/<post_id>``

.. figure:: images/post.png
   :align: center

   Post View

The original submitter of the post or a moderator of the tag can edit
or delete posts

.. figure:: images/edit_post.png
   :align: center

   Post Editing

