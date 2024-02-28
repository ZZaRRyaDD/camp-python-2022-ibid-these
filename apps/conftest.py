from django.test.client import Client

from rest_framework import test

import pytest

from apps.users.factories import UserFactory
from apps.users.models import User


@pytest.fixture
def api_client() -> test.APIClient:
    """Create api client."""
    return test.APIClient()


@pytest.fixture
def user(django_db_setup, django_db_blocker):
    """Module-level fixture for user."""
    with django_db_blocker.unblock():
        created_user = UserFactory()
        yield created_user
        created_user.delete()


@pytest.fixture
def auth_client(user: User, client: Client):
    """Fixture for authorized client."""
    client.force_login(user=user)
    return client
