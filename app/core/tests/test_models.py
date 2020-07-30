from django.test import TestCase
from django.contrib.auth import get_user_model


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful\
        メールで新しいユーザーを作成するテストは成功しています"""
        email = 'test@japandev.com'
        password = 'Testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for a new user is normalized\
        新しいユーザーのためのメールが正規化されているかどうかをテストする"""
        email = 'test@JAPANDEV.COM'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_usre_invalid_email(self):
        """Test creating user with no email raises error\
        メールのないユーザーを作成するテストでエラーが発生する"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_new_superuser(self):
        """Test creating a new superuser\
        新しいスーパーユーザーを作成するテスト"""
        user = get_user_model().objects.create_superuser(
            'test@japandev.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
