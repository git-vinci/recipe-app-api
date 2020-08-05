from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')


def create_user(**params):
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the users API (public)
    ユーザーAPIのテスト (公開)"""

    def setUp(self):
        self.client = APIClient()

    def test_create_valid_user_success(self):
        """Test creating user with valid payload is successful
        有効なペイロードを使用してユーザーを作成するテストは成功しました。"""
        payload = {
            'email': 'test@japandev.com',
            'password': 'testpass',
            'name': 'Test name'
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**res.data)
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_exists(self):
        """Test creatinga user that alreagy exists fails
        ユーザが存在するかどうかのテストに失敗する"""
        paylaod = {'email': 'test@japandev.com', 'password': 'testpass'}
        create_user(**paylaod)

        res = self.client.post(CREATE_USER_URL, paylaod)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """Test that password must be more than 5 characters"""
        payload = {'email': 'test@japandev.com', 'password': 'pw'}
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test that token is created for the user
        トークンがユーザー用に作成されていることをテストする"""
        payload = {'email': 'test@japandev.com', 'password': 'testpass'}
        create_user(**payload)
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_invalid_credentials(self):
        """Test that token is not created if invalid credentials are given
        無効な認証情報が与えられた場合にトークンが作成されないことをテストする"""
        create_user(email='test@japnadev.com', password="testpass")
        payload = {'email': 'test@japandev.com', 'password': 'wrong'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_no_user(self):
        """Test that token is not cerated if user doesn't exist
        ユーザが存在しない場合にトークンがセレーションされないことをテストする"""
        payload = {'email': 'test@japandev.com', 'password': 'testpass'}
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """Test that email and password are required
        電子メールとパスワードが必要であることをテスト"""
        res = self.client.post(TOKEN_URL, {'email': 'one', 'password': ''})
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
