import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question
from django.urls import reverse


# 按照惯例，Django 应用的测试应该写在应用的 tests.py 文件里。测试系统会自动的在所有文件里寻找并执行以 test 开头的测试函数。
class QuestionModelTests(TestCase):
    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is older than 1 day.
        """
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """
        was_published_recently() returns True for questions whose pub_date
        is within the last day.
        """
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        # reverse函数的作用就是用来进行URL反转
        response = self.client.get(reverse("t2020_polls:index"))
        self.assertEqual(response.status_code, 200)
        print("response1:", response)
        self.assertContains(response, "No t2020_polls are available.")
        print("response.context1:", response.context["latest_question_list"])
        self.assertQuerySetEqual(
            qs=response.context["latest_question_list"],
            values=[]
        )

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("t2020_polls:index"))
        print("question2:", question)
        print("response2:", response)
        print("response.context2:", response.context["latest_question_list"])
        self.assertQuerySetEqual(
            qs=response.context["latest_question_list"],
            values=[question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("t2020_polls:index"))
        print("response3:", response)
        print("response.context3:", response.context["latest_question_list"])
        self.assertContains(response, "No t2020_polls are available.")
        self.assertQuerySetEqual(
            qs=response.context["latest_question_list"],
            values=[]
        )

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("t2020_polls:index"))
        print("question4:", question)
        print("response4:", response)
        print("response.context4:", response.context["latest_question_list"])
        self.assertQuerySetEqual(
            qs=response.context["latest_question_list"],
            values=[question],
        )

    def test_two_past_questions(self):
        """
        The questions index page may display multiple questions.
        """
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse("t2020_polls:index"))
        print("question1:", question1, "\n", "question2:", question2)
        print("response:", response)
        print("response.context:", response.context["latest_question_list"])
        self.assertQuerySetEqual(
            qs=response.context["latest_question_list"],
            values=[question2, question1],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("t2020_polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        print("response5:", response)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("t2020_polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        print("response6:", response)
        self.assertContains(response, past_question.question_text)
