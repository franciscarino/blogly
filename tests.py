from unittest import TestCase

from app import app, db
from models import DEFAULT_IMAGE_URL, User, Post

# Let's configure our app to use a different database for tests
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///blogly_test"

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

# Create our tables (we do this here, so we only create the tables
# once for all tests --- in each test, we'll delete the data
# and create fresh new clean test data

db.create_all()


class UserViewTestCase(TestCase):
    """Test views for users."""

    def setUp(self):
        """Create test client, add sample data."""

        # As you add more models later in the exercise, you'll want to delete
        # all of their records before each test just as we're doing with the
        # User model below.
        breakpoint()
        User.query.delete()

        self.client = app.test_client()

        test_user = User(
            first_name="test_first",
            last_name="test_last",
            img_url=None,
        )

        second_user = User(
            first_name="test_first_two",
            last_name="test_last_two",
            img_url=None,
        )

        breakpoint()

        db.session.add_all([test_user, second_user])
        db.session.commit()

        # We can hold onto our test_user's id by attaching it to self (which is
        # accessible throughout this test class). This way, we'll be able to
        # rely on this user in our tests without needing to know the numeric
        # value of their id, since it will change each time our tests are run.
        self.user_id = test_user.id

    def tearDown(self):
        """Clean up any fouled transaction."""
        db.session.rollback()

    def test_list_users(self):
        """Tests users list."""
        with self.client as c:
            resp = c.get("/users")
            self.assertEqual(resp.status_code, 200)
            html = resp.get_data(as_text=True)
            self.assertIn("test_first", html)
            self.assertIn("test_last", html)

    def test_new_user_form(self):
        """Test new user form is correct."""
        with self.client as c:
            resp = c.get("/users/new")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Create a user', html)

    # def test_new_user(self):
    #     """Test submitting a new user will redirect."""
    #     with self.client as c:
    #         resp = c.post("/users/new", data={'first-name': 'Spin',
    #                                     'last-name': "Drift",
    #                                     'img-url': DEFAULT_IMAGE_URL})
    #         self.assertEqual(resp.status_code, 302)
    #         self.assertEqual(resp.location, '/users')

    def test_new_user_redirect(self):
        """Test submitting a new user redirects correctly with new user info."""
        with self.client as c:
            resp = c.post("/users/new", data={'first-name': 'Spin',
                                        'last-name': "Drift",
                                        'img-url': DEFAULT_IMAGE_URL})
            resp = c.get("/users", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn('Spin', html)


# class PostViewTestCase(TestCase):
#     """Test views for posts."""

#     def setUp(self):
#         """Create test client, add sample data."""

#         Post.query.delete()

#         self.client = app.test_client()

#         test_user = User(
#             first_name="test_first",
#             last_name="test_last",
#             img_url=None,
#         )

#         test_post = Post(
#             title = "test_title",
#             content = "test_content",
#             user_id = 1
#         )

#         test_post_two = Post(
#             title = "test_title_two",
#             content = "test_content_two",
#             user_id = 1
#         )

#         db.session.add_all([test_user, test_post, test_post_two])
#         db.session.commit()


#         self.user_id = test_user.id
#         self.post_id = test_post.id

#     def tearDown(self):
#         """Clean up any fouled transaction."""
#         db.session.rollback()

#     def test_list_posts(self):
#         """Tests posts list."""
#         with self.client as c:
#             resp = c.get("/users/1")
#             self.assertEqual(resp.status_code, 200)
#             html = resp.get_data(as_text=True)
#             self.assertIn("test_title", html)
#             self.assertIn("test_title_two", html)