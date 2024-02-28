from decimal import Decimal

import arrow
import factory

from apps.users.factories import UserFactory

from . import models

COUNT_IMAGES = 3


class CategoryFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Category instance."""

    name = factory.Faker(
        "month_name",
    )

    class Meta:
        model = models.Category
        django_get_or_create = (
            "name",
        )


class LotFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Lot instance."""

    name = factory.Faker(
        "currency_name",
    )
    user = factory.SubFactory(
        UserFactory,
    )
    description = factory.Faker(
        "catch_phrase",
    )
    category = factory.SubFactory(
        CategoryFactory,
    )
    start_price = factory.Faker(
        "pydecimal",
        left_digits=9,
        right_digits=2,
        positive=True,
        min_value=1.0,
    )
    bid_increment = factory.Faker(
        "pydecimal",
        left_digits=9,
        right_digits=2,
        positive=True,
        min_value=1.0,
    )
    redemption_price = factory.LazyAttribute(
        lambda obj: obj.start_price + Decimal("2.0"),
    )
    status = models.Lot.Status.DRAFT
    end_date = arrow.utcnow().shift(days=+1).datetime

    @factory.post_generation
    def image(self, create, extracted, **kwargs):
        """Create images for lot."""
        if not create:
            return
        images = extracted if extracted is not None else (
            LotImageFactory(lot=self) for _ in range(COUNT_IMAGES)
        )
        self.images.add(*images)

    class Meta:
        model = models.Lot


class LotImageFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Images instance."""

    image = factory.django.ImageField(
        color="green",
    )
    lot = factory.SubFactory(
        LotFactory,
    )

    class Meta:
        model = models.LotImage


class BidFactory(factory.django.DjangoModelFactory):
    """Factory for generates test Bid instance."""

    bid = factory.Faker(
        "pydecimal",
        left_digits=9,
        right_digits=2,
        positive=True,
        min_value=1.0,
    )
    created = arrow.now().shift(days=-1).datetime
    user = factory.SubFactory(
        UserFactory,
    )
    lot = factory.SubFactory(
        LotFactory,
    )

    class Meta:
        model = models.Bid
