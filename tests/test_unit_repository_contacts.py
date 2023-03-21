import unittest
from datetime import datetime, timedelta
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import Contact, User
from src.schemas import ContactModel, ContactFavoriteStatus
from src.repository.contacts import (
    get_contacts,
    get_contact,
    create_contact,
    remove_contact,
    update_contact,
    update_favorite_contact,
    get_birthday_contacts
)


class TestContacts(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = User(id=1, email='usertest@gmail.com')

    async def test_get_contacts(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=None, first_name=None, last_name=None, email=None,
                                    user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_favorite(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=False, first_name=None, last_name=None, email=None,
                                    user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_first_name(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=None, first_name="User", last_name=None, email=None,
                                    user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_last_name(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=None, first_name=None, last_name="Contact", email=None,
                                    user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_email(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=None, first_name=None, last_name=None,
                                    email='usertest@gmail.com', user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_favorite_first_name(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=False, first_name='User', last_name=None, email=None,
                                    user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_favorite_last_name(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=False, first_name=None, last_name='Contact',
                                    email=None, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_favorite_email(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=False, first_name=None, last_name=None,
                                    email='usertest@gmail.com', user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_first_name_last_name(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=None, first_name='User', last_name='Contact',
                                    email=None, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_first_name_email(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=None, first_name='User', last_name=None,
                                    email='usertest@gmail.com', user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_last_name_email(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=None, first_name=None, last_name="Contact",
                                    email='usertest@gmail.com', user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_favorite_first_name_last_name(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=False, first_name='User', last_name='Contact',
                                    email=None, user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_favorite_first_name_email(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=False, first_name='User', last_name=None,
                                    email='usertest@gmail.com', user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_favorite_last_name_email(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=False, first_name=None, last_name='Contact',
                                    email='usertest@gmail.com', user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_first_name_last_name_email(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=None, first_name='User', last_name='Contact',
                                    email='usertest@gmail.com', user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contacts_with_all(self):
        contacts = [Contact(), Contact(), Contact()]
        self.session.query().filter().filter().filter().filter().filter().limit().offset().all.return_value = contacts
        result = await get_contacts(limit=10, offset=0, favorite=False, first_name='User', last_name='Contact',
                                    email='usertest@gmail.com', user=self.user, db=self.session)
        self.assertEqual(result, contacts)

    async def test_get_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_get_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_contact(self):
        body = ContactModel(first_name='User', last_name='Contact', email='usertest@gmail.com',
                            birth_date=datetime.now())
        result = await create_contact(body=body, user=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.birth_date, body.birth_date)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_contact_found(self):
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_remove_contact_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_contact(contact_id=1, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_contact_found(self):
        body = ContactModel(first_name='User', last_name='Contact', email='usertest@gmail.com',
                            birth_date=datetime.now())
        contact = Contact(first_name='Contact', last_name='User', email='contacttest@gmail.com',
                          birth_date=datetime.now())
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_contact_not_found(self):
        body = ContactModel(first_name='User', last_name='Contact', email='usertest@gmail.com',
                            birth_date=datetime.now())
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_favorite_contact_found(self):
        body = ContactFavoriteStatus(favorite=True)
        contact = Contact()
        self.session.query().filter().first.return_value = contact
        self.session.commit.return_value = None
        result = await update_favorite_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertEqual(result, contact)

    async def test_update_favorite_contact_not_found(self):
        body = ContactFavoriteStatus(done=True)
        self.session.query().filter().first.return_value = None
        self.session.commit.return_value = None
        result = await update_favorite_contact(contact_id=1, body=body, user=self.user, db=self.session)
        self.assertIsNone(result)

    # async def test_get_birthday_contacts(self):
    #     contacts = [Contact(), Contact(), Contact()]
    #     result = await get_birthday_contacts(user=self.user, db=self.session)
    #     self.assertEqual(result, contacts)


if __name__ == '__main__':
    unittest.main()
