import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel
from src.repository.users import (
    get_user_by_email,
    create_user,
    update_token,
    confirmed_email,
    update_avatar
)


class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, email='usertest@gmail.com', confirmed=False)

    async def test_get_user_by_email_found(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_by_email_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user_by_email(email=self.user.email, db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserModel(username='Username', email='usertest@gmail.com', password='password')
        result = await create_user(body=body, db=self.session)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_token_with_token(self):
        await update_token(user=self.user, db=self.session, token='token')
        self.assertIsNotNone(self.user.refresh_token)

    async def test_update_token_without_token(self):
        await update_token(user=self.user, db=self.session, token=None)
        self.assertIsNone(self.user.refresh_token)

    async def test_confirmed_email(self):
        result = await confirmed_email(email=self.user.email, db=self.session)
        self.assertTrue(result.confirmed)

    async def test_update_avatar(self):
        url = 'url'
        result = await update_avatar(email=self.user.email, db=self.session, url=url)
        self.assertEqual(result.avatar, url)


if __name__ == '__main__':
    unittest.main()
