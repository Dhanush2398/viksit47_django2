from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from datetime import date, timedelta
from .models import (
    Profile, Mock, Question, Option, MockResult,
    StudyMaterial, StudyMaterialItem, Author, CourseSubscription
)

class ProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="dhanush", password="testpass")
        self.profile = Profile.objects.create(
            user=self.user,
            full_name="Dhanush Aradhya",
            whatsapp_number="9999999999",
            gmail="test@example.com",
            district_name="Mysuru",
            taluk_name="T Narasipura",
            college_name="Agri College"
        )

    def test_profile_str(self):
        self.assertEqual(str(self.profile), "Dhanush Aradhya")


class MockExamTest(TestCase):
    def setUp(self):
        self.mock = Mock.objects.create(
            course="agri_quota",
            title="Sample Mock Test",
            time_limit=30,
            difficulty="easy"
        )
        self.question = Question.objects.create(mock=self.mock, text="What is 2+2?")
        self.option1 = Option.objects.create(question=self.question, text="4", is_correct=True)
        self.option2 = Option.objects.create(question=self.question, text="3", is_correct=False)

    def test_mock_str(self):
        self.assertIn("Sample Mock Test", str(self.mock))

    def test_question_str(self):
        self.assertEqual(str(self.question), "What is 2+2?")

    def test_option_str_correct(self):
        self.assertIn("Correct", str(self.option1))

    def test_option_str_wrong(self):
        self.assertIn("Wrong", str(self.option2))


class MockResultTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.mock = Mock.objects.create(title="Math Test", course="agri_quota")
        self.result = MockResult.objects.create(user=self.user, mock=self.mock, total=5, correct=3, attempted=4)

    def test_score_calculated(self):
        self.result.refresh_from_db()
        self.assertEqual(self.result.score, 60.0)

    def test_result_str(self):
        self.assertIn("testuser", str(self.result))


class StudyMaterialTest(TestCase):
    def setUp(self):
        self.material = StudyMaterial.objects.create(course="agri_quota", title="Soil Science")
        self.item = StudyMaterialItem.objects.create(
            study_material=self.material,
            title="Soil Layers",
            description="Topsoil, subsoil, bedrock"
        )

    def test_study_material_str(self):
        self.assertIn("Soil Science", str(self.material))

    def test_study_material_item_str(self):
        self.assertIn("Soil Layers", str(self.item))


class AuthorTest(TestCase):
    def setUp(self):
        self.author = Author.objects.create(name="Dr. Smith")

    def test_author_str(self):
        self.assertEqual(str(self.author), "Dr. Smith")


class CourseSubscriptionTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="subuser", password="testpass")
        self.subscription = CourseSubscription.objects.create(
            user=self.user,
            course_slug="agri_quota",
            end_date=date.today() + timedelta(days=365),
            uu_id="abc123",
            amount=2000,
            is_paid=True
        )

    def test_subscription_str(self):
        self.assertIn("subuser", str(self.subscription))


# ----------------------
# ✅ Basic View Tests
# ----------------------
class ViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="viewuser", password="testpass")

    def test_about_page(self):
        response = self.client.get(reverse("about"))
        self.assertEqual(response.status_code, 200)

    def test_contact_page(self):
        response = self.client.get(reverse("contact"))
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.client.get(reverse("register"))
        self.assertEqual(response.status_code, 200)

    def test_profile_redirect_if_not_logged_in(self):
        response = self.client.get(reverse("profile"))
        self.assertEqual(response.status_code, 302)  # redirect to login
