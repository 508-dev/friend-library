"""
Pytest configuration for stuff4friends.
"""

import pytest


@pytest.fixture
def user_factory(db):
    """Factory for creating test users."""
    from library.models import User

    def create_user(
        username="testuser",
        password="testpass123",
        is_approved=True,
        **kwargs,
    ):
        user = User.objects.create_user(
            username=username,
            password=password,
            is_approved=is_approved,
            **kwargs,
        )
        return user

    return create_user


@pytest.fixture
def approved_user(user_factory):
    """A pre-created approved user."""
    return user_factory()


@pytest.fixture
def item_factory(db, approved_user):
    """Factory for creating test items."""
    from library.models import Item

    def create_item(
        owner=None,
        title="Test Item",
        **kwargs,
    ):
        return Item.objects.create(
            owner=owner or approved_user,
            title=title,
            **kwargs,
        )

    return create_item
