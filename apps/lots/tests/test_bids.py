from decimal import Decimal

from django.urls import reverse_lazy

from rest_framework import status

from ...users.models import User
from ..factories import LotFactory
from ..forms import BidCreateForm
from ..models import Lot


def test_bid_less_than_start_price_lot(
    user: User,
) -> None:
    """Test error if bid less than start price lot."""
    lot = LotFactory.create(
        user=user,
        start_price=Decimal("13.0"),
        bid_increment=Decimal("2.0"),
    )
    bid_data = {
        "user": user,
        "lot": lot,
        "bid": Decimal("5.0"),
    }
    form = BidCreateForm(data=bid_data, lot=lot)
    error_message = "Start price can not be more or equal than bid price"
    assert not form.is_valid()
    expected_message = form.errors["bid"].as_data()[0].message
    assert expected_message == error_message


def test_bid_more_than_start_price_lot(
    user: User,
) -> None:
    """Test error if bid more than start price lot."""
    lot = LotFactory.create(
        user=user,
        start_price=Decimal("13.0"),
        bid_increment=Decimal("2.0"),
    )
    bid_data = {
        "user": user,
        "lot": lot,
        "bid": Decimal("20.0"),
    }
    form = BidCreateForm(data=bid_data, lot=lot)
    assert form.is_valid()


def test_create_bid(
    auth_client,
    user: User,
    client,
) -> None:
    """Test bid creation."""
    lot = LotFactory.create(
        user=user,
        status=Lot.Status.IN_PROCCESS,
        start_price=Decimal("13.0"),
        bid_increment=Decimal("2.0"),
    )
    bid = lot.start_price + lot.bid_increment
    response = auth_client.post(
        reverse_lazy("lots:details", kwargs={"pk": lot.pk}),
        data={
            "bid": bid,
        },
    )
    assert response.status_code == status.HTTP_302_FOUND
    assert lot.bids.filter(user=user, bid=bid).exists()
