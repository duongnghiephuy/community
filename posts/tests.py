import datetime
from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Community
from polls.models import Question, Choice
from django.urls import reverse
from django.test import Client
from posts.models import Post, Order
from django.core.files.uploadedfile import SimpleUploadedFile

# Create your tests here.


class PostModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # user is in the group below we want to test
        cls.user = User.objects.create_user(username="testuser", password="12345")
        # user1 is also in the group below we want to test
        cls.user1 = User.objects.create(username="testuser1", password="12345")

        cls.community = Community.objects.create(
            name="Test_Community",
            description="This is a community for test",
        )
        cls.client = Client()

        post_title = "Test post"
        post_content = "This is a just a test"

        post_image = SimpleUploadedFile(
            name="testpimg", content=open("media\postimages\lime.webp", "rb").read()
        )
        schedule_from = timezone.now() + datetime.timedelta(days=2)
        schedule_to = timezone.now() + datetime.timedelta(days=2, minutes=30)

        cls.post = Post.objects.create(
            post_title=post_title,
            post_content=post_content,
            img_width=20,
            img_height=20,
            post_image=post_image,
            schedule_from=schedule_from,
            schedule_to=schedule_to,
            community=cls.community,
        )

        Order.objects.create(post=cls.post, participant=cls.user, role=Order.HOST)
        Order.objects.create(post=cls.post, participant=cls.user1, role=Order.SHARER)

    def setUp(self):
        self.client.login(username="testuser", password="12345")

    def test_host(self):
        self.assertEqual(self.post.host, self.user)
        self.assertNotEqual(self.post, self.user1)
