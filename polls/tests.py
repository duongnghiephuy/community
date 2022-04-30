from django.test import TestCase
from django.contrib.auth.models import User
from django.utils import timezone
from accounts.models import Community
from polls.models import Question, Choice
from django.urls import reverse
from django.test import Client

# Create your tests here.


class QuestionModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # user is in the group we want to test
        cls.user = User.objects.create_user(username="testuser", password="12345")
        # @user1 is not in the group we want to test
        cls.user1 = User.objects.create(username="testuser1", password="12345")

        cls.community = Community.objects.create(
            name="Test_Community",
            description="This is a community for test",
        )

        # Create a live question and choices
        question_text = "Test Question"
        pub_date = timezone.now()
        cls.question = Question.objects.create(
            question_text=question_text,
            pub_date=pub_date,
            closed=False,
            author=cls.user,
            community=cls.community,
        )

        for choice_text in ["Choice 1", "Choice 2"]:
            Choice.objects.create(question=cls.question, choice_text=choice_text)

        cls.client = Client()

    def setUp(self):
        self.client.login(username="testuser", password="12345")

    def test_is_voter(self):
        self.assertIs(self.question.is_voter(self.user), True)
        self.assertIs(self.question.is_voter(self.user1), False)

    # test failed vote without data
    def test_no_data_votemodal(self):

        # login required for all votemodal test

        response = self.client.post(
            reverse("polls:votemodal", kwargs={"question_id": self.question.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context["error_message"], "You didn't select a choice"
        )

    # test vote with data
    def test_data_votemodal(self):
        response = self.client.post(
            reverse(
                "polls:votemodal",
                kwargs={"question_id": self.question.id},
            ),
            data={"choice": 1},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["error_message"], None)

        # test vote after changing choice

        response = self.client.post(
            reverse(
                "polls:votemodal",
                kwargs={"question_id": self.question.id},
            ),
            data={"choice": 2},
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context["error_message"], "You changed your vote")
