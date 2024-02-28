from decimal import Decimal

from django.core.exceptions import ValidationError
from django.test.client import Client
from django.urls import reverse, reverse_lazy

from rest_framework import status

import arrow
import pytest

from ...users.factories import UserFactory
from ...users.models import User
from ..factories import CategoryFactory, LotFactory, LotImageFactory
from ..models import Category, Lot


def test_end_date_later_than_now(
    user: User,
) -> None:
    """Test if end date later than now."""
    lot = LotFactory.build(user=user)
    lot.clean()


def test_end_date_earlier_than_now(
    user: User,
) -> None:
    """Test error raises if end date earlier than now."""
    lot = LotFactory.build(
        user=user,
        end_date=arrow.utcnow().shift(days=-1).datetime,
    )
    match = (r"End date can't be earlier that now")
    with pytest.raises(ValidationError, match=match):
        lot.clean()


def test_redemption_price_more_or_equal_than_start_price(
    user: User,
) -> None:
    """Test if redemption price more or equal than start price."""
    lot = LotFactory.build(
        user=user,
        start_price=Decimal("12.0"),
        redemption_price=Decimal("12.0"),
    )
    lot.clean()


def test_redemption_price_less_than_start_price(
    user: User,
) -> None:
    """Test error raises if redemption price less than start price."""
    lot = LotFactory.build(
        user=user,
        start_price=Decimal("13.0"),
        redemption_price=Decimal("12.0"),
    )
    match = (r"Redemption price can not be less then start price")
    with pytest.raises(ValidationError, match=match):
        lot.clean()


@pytest.mark.parametrize(
    argnames=["status_lot", "status_response"],
    argvalues=[
        [
            Lot.Status.FINISHED,
            status.HTTP_403_FORBIDDEN,
        ],
        [
            Lot.Status.IN_PROCCESS,
            status.HTTP_403_FORBIDDEN,
        ],
        [
            Lot.Status.DRAFT,
            status.HTTP_200_OK,
        ],
    ],
)
def test_owner_cant_update_lot_in_statuses(
    status_lot: str,
    status_response: str,
    user: User,
    client: Client,
) -> None:
    """Test error with permissions of some users."""
    lot = LotFactory.create(
        user=user,
        status=status_lot,
    )
    client.force_login(user=user)
    response = client.post(
        reverse("lots:update", kwargs={"pk": lot.pk}),
    )
    assert response.status_code == status_response


def test_not_owner_can_update_lot(
    user: User,
    client: Client,
) -> None:
    """Test error with permissions of some users."""
    lot = LotFactory.create(
        user=user,
    )
    another_user = UserFactory.create()
    client.force_login(user=another_user)
    response = client.post(
        reverse("lots:update", kwargs={"pk": lot.pk}),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_banned_user_cant_create_lot(
    client: Client,
) -> None:
    """Test error with permissions of banned users."""
    user = UserFactory(can_create_lots=False)
    client.force_login(user=user)
    response = client.get(
        reverse_lazy("lots:create"),
    )
    assert response.status_code == status.HTTP_403_FORBIDDEN


def test_create_lot(
    user: User,
    client: Client,
) -> None:
    """Test lot creation."""
    CategoryFactory.create()
    lot = LotFactory.build(
        user=user,
        category=Category.objects.first(),
    )
    image = LotImageFactory.create()
    client.force_login(user=user)
    response = client.post(
        reverse_lazy("lots:create"),
        data={
            "name": lot.name,
            "description": lot.description,
            "category": Category.objects.first().id,
            "start_price": lot.start_price,
            "bid_increment": lot.bid_increment,
            "redemption_price": lot.redemption_price,
            "status": lot.status,
            "end_date": lot.end_date,
            "images-TOTAL_FORMS": ["1"],
            "images-INITIAL_FORMS": ["0"],
            "images-0-image": image.image,
            "images-0-DELETE": "",
        },
    )
    assert response.status_code == status.HTTP_302_FOUND
    assert Lot.objects.filter(
        name=lot.name,
        description=lot.description,
        category=lot.category,
        start_price=lot.start_price,
        bid_increment=lot.bid_increment,
        redemption_price=lot.redemption_price,
        status=lot.status,
        end_date=lot.end_date,
    ).exists()
    assert Lot.objects.get(
        name=lot.name,
        description=lot.description,
        category=lot.category,
        start_price=lot.start_price,
        bid_increment=lot.bid_increment,
        redemption_price=lot.redemption_price,
        status=lot.status,
        end_date=lot.end_date,
    ).images.exists()


def test_not_owner_user_cant_see_lot_in_status_draft(
    user: User,
    client: Client,
) -> None:
    """Test error with permissions of some users."""
    lot = LotFactory.create(
        user=user,
        status=Lot.Status.DRAFT,
    )
    another_user = UserFactory.create()
    client.force_login(user=another_user)
    response = client.get(
        reverse("lots:details", kwargs={"pk": lot.pk}),
    )
    assert response.status_code == status.HTTP_302_FOUND


@pytest.mark.parametrize(
    argnames=["status_lot", "status_response"],
    argvalues=[
        [
            Lot.Status.FINISHED,
            status.HTTP_200_OK,
        ],
        [
            Lot.Status.IN_PROCCESS,
            status.HTTP_200_OK,
        ],
    ],
)
def test_not_owner_user_can_see_lot_in_statuses(
    user: User,
    status_lot: str,
    status_response: str,
    client: Client,
) -> None:
    """Test error with permissions of some users."""
    lot = LotFactory.create(
        user=user,
        status=status_lot,
    )
    another_user = UserFactory.create()
    client.force_login(user=another_user)
    response = client.get(
        reverse("lots:details", kwargs={"pk": lot.pk}),
    )
    assert response.status_code == status_response


@pytest.mark.parametrize(
    argnames=["status_lot", "status_response"],
    argvalues=[
        [
            Lot.Status.DRAFT,
            status.HTTP_200_OK,
        ],
        [
            Lot.Status.IN_PROCCESS,
            status.HTTP_200_OK,
        ],
        [
            Lot.Status.FINISHED,
            status.HTTP_200_OK,
        ],
    ],
)
def test_owner_can_see_lot_in_statuses(
    user: User,
    status_lot: str,
    status_response: str,
    client: Client,
) -> None:
    """Test error with permissions of some users."""
    lot = LotFactory.create(
        user=user,
        status=status_lot,
    )
    this_user = User.objects.get(id=lot.user.id)
    client.force_login(user=this_user)
    response = client.get(
        reverse("lots:details", kwargs={"pk": lot.pk}),
    )
    assert response.status_code == status_response


def test_add_favorites(
    user: User,
    client: Client,
) -> None:
    """Test add lot in favorites."""
    lot = LotFactory.create(
        user=user,
    )
    client.force_login(user=user)
    client.post(
        reverse("lots:action_favorites_lot", kwargs={"pk": lot.pk}),
    )
    assert lot in user.favorite_lots.all()


def test_remove_favorites(
    user: User,
    client: Client,
) -> None:
    """Test remove lot for favorites."""
    lot = LotFactory.create(
        user=user,
    )
    user.favorite_lots.add(lot)
    client.force_login(user=user)
    client.post(
        reverse("lots:action_favorites_lot", kwargs={"pk": lot.pk}),
    )
    assert lot not in user.favorite_lots.all()
