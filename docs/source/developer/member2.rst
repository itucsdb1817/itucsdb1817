Parts Implemented by Efe Hakan Gençoğlu
================================

**Tags**
--------

This table provides common tags for posts to be submitted under.
All posts must be submitted with a tag.
It does not reference any other tables.

1 - Table Creation
~~~~~~~~~~~~~~~~~~

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

2 - Routes
~~~~~~~~~~

All viewers can view a tag, but only tag creators and moderators selected
by the tag creator and the other mods are allowed to access the
moderation page.

**Tag Creation**

User must be logged in to create a tag.
Route for creating a post is ``/tag_create``

.. code-block:: python

        @tag_pages.route('/tag_create', methods = ['GET', 'POST'])
        def tag_create():
            if not check.logged_in():
                error_context = {
                    'error_name': "403 Forbidden",
                    'error_info': "You may not create a tag without an account. Please log in or create an account"
                }
                return render_template('error.html', **error_context)
            else:
                form = TagCreationForm()
                if form.validate_on_submit():
                    tag = Tag()
                    mod = TagModerator()

                    # TODO: tag name sanitization
                    tag.title = form.title.data
                    tag.date = datetime.now()
                    tag.subscriber_amount = 0
                    tag.is_banned = False
                    tag.description = form.description.data
                    tag.rules = form.rules.data

                    tag.save()

                    # exact same date of creation denotes original creator
                    mod.date = tag.date
                    mod.user_id = int(session['user_id'])
                    mod.tag_id = tag.id

                    mod.save()

                    flash('New tag created')
                    # TODO: Redirect to tag page
                    return render_template('tag_create.html', form=form)
                else:
                    return render_template('tag_create.html', form=form)


**Main Tag View**

Anyone can see the post history of the tag and all the posts that are not deleted,
through the route ``/t/<tag_name>``. It utilizes the pagination method in the model for the tag.

.. code-block:: python

        @tag_pages.route('/t/<string:tag_name>', methods=['GET'])
        def tag_view(tag_name):
            tag = Tag(tag_name)
            posts = True
            # existance of the attributes _ORIGINAL_ATTR denotes the model instance
            # is not new and interfaces an entry in table
            if not hasattr(tag, '_ORIGINAL_ATTR'):
                error_context = {
                    'error_name': "404 Not Found",
                    'error_info': "The tag you tried to access does not exist, but you can create this tag."
                }
                return render_template('error.html', **error_context)
            
            # TODO: Implement tag page and pagination 
            
            page_index = int(request.args.get('page') or 1)
            if not isinstance(page_index, int):
                page_index = 1
            if page_index <= 0:
                page_index = 1
            
            context = {  
                'tag_info': {
                    'title':        tag.title,
                    'rules':        tag.rules,
                    'description':  tag.description
                }
            }
            context['pagination'] = tag.paginate(page_index)
            return render_template('tag.html', **context)


3 - Special Methods and Queries
~~~~~~~~~~~~~~~~~~~~~~~

Pagination
^^^^^^^^^^

.. code-block:: python

        def paginate(self, page, page_size=20):
            """
            This method paginates the entries in database.
            """
            assert page > 0
            with db.connect(current_app.config['DB_URL']) as conn:
                # TODO: Selection of sorting
                cursor = conn.cursor()
                cursor.execute(f"SELECT COUNT(id) FROM posts WHERE tag_id={self.id}")
                count = cursor.fetchone()[0]
                if count == 0:
                    # table is empty, abort 
                    pagination = {}
                    pagination['page_number'] = 1
                    pagination['last_page_number'] = 1
                    pagination['posts'] = []  
                    return pagination
                # Normalize page index if it exceeds max page count
                pagination = {}
                max_page_count = int(ceil(count / page_size))  
                if max_page_count < page:
                    page = max_page_count
                pagination['page_number'] = page
                pagination['last_page_number'] = max_page_count
                pagination['posts'] = []
                cursor.execute(f"SELECT * FROM posts WHERE tag_id={self.id}")
                for i in range(page):
                    post_tuples = cursor.fetchmany(page_size)
                    if post_tuples is None:
                        raise IndexError('No set of posts left to render')
                for post_tuple in post_tuples:
                    post = Post(post_tuple)
                    info = {
                        'title':    post.title,
                        'id':       post.id,
                        'user':     User(post.user_id).username,
                        'vote':     post.current_vote,
                        'date':     post.date
                    }
                    pagination['posts'].append(info)
                cursor.close()
                return pagination

Posts
-----

Posts are submitted by logged in users.
Content of a post can be text, image, gif, link.
Posts are markdown enabled.

1 - Table Creation
~~~~~~~~~~~~~~~~~~

.. code-block:: sql

        CREATE TABLE posts (
            id serial  NOT NULL,
            user_id int  NOT NULL,
            tag_id int NOT NULL,
            date timestamp  NOT NULL,
            title varchar(256)  NOT NULL,
            content_type varchar(32)  NOT NULL,
            content text  NOT NULL,
            content_html text NOT NULL,
            is_external boolean  NOT NULL,
            current_vote int  NOT NULL,
            is_banned boolean  NOT NULL,
            comment_count int  NOT NULL,
            CONSTRAINT posts_pk PRIMARY KEY (id)
        );


* ``user_id`` ``FK(users)`` User who created the post.
* ``tag_id`` ``FK(tags)`` The tag the post was submitted to.
* ``content_type`` text, image or link.
* ``content`` Markdown content.
* ``content_html`` Rendered Markdown content.

2 - Routes
~~~~~~~~~~

* ``/post/submit`` - Post submission
* ``/post/<post_id>`` - Main view
* ``/post/<post_id>/edit`` - Edit post (Only OP and Mods)
* ``/post/<post_id>/delete`` - Delete post (Only OP and Mods)


Comments
--------

Comments refernce posts, and go under posts.
Markdown enabled


1 - Table Creation
~~~~~~~~~~~~~~~~~~

.. code-block:: sql

        CREATE TABLE comments (
            id serial  NOT NULL,
            user_id int  NOT NULL,
            post_id int  NOT NULL,
            content_type varchar(32)  NOT NULL,
            content text  NOT NULL,
            content_html text NOT NULL,
            is_external boolean  NOT NULL,
            date timestamp  NOT NULL,
            current_vote int  NOT NULL,
            CONSTRAINT comments_pk PRIMARY KEY (id)
        );


* ``user_id`` ``FK(users)`` User who created the post.
* ``tag_id`` ``FK(tags)`` The tag the post was submitted to.
* ``content_type`` text, image or link.
* ``content`` Markdown content.
* ``content_html`` Rendered Markdown content.

2 - Routes
~~~~~~~~~~

* ``/post/<post_id>`` - Comment submission
* ``/comment/<post_id>/edit`` - Edit comment (Only OP and Mods)
* ``/comment/<post_id>/delete`` - Delete comment (Only OP and Mods)
