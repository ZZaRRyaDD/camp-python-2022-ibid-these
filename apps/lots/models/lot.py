from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

import arrow

from apps.core.fields import PriceField
from apps.core.models import BaseModel


class Lot(BaseModel):
    """Model for lot.

    Lot statuses:
        Finished: lot in closed and read-only
        In Proccess: lot in active
        Draft: lot not created
    """

    class Status(models.TextChoices):
        """Class choices."""

        FINISHED = "FINISHED", _("Finished")
        IN_PROCCESS = "IN_PROCCESS", _("In Proccess")
        DRAFT = "DRAFT", _("Draft")

    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="lot",
    )
    name = models.CharField(
        max_length=256,
        verbose_name=_("Name"),
    )
    description = models.TextField(
        verbose_name=_("Description"),
    )
    interest_users = models.ManyToManyField(
        "users.User",
        related_name="favorite_lots",
    )
    category = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
        verbose_name=_("Category"),
        related_name="lots",
    )
    start_price = PriceField(
        verbose_name=_("Start price"),
    )
    bid_increment = PriceField(
        verbose_name=_("Bid increment"),
        validators=[
            MinValueValidator(1.0),
        ],
        help_text=_("Different between last and current bids"),
    )
    redemption_price = PriceField(
        verbose_name=_("Redemption price"),
        null=True,
        blank=True,
    )
    status = models.CharField(
        max_length=11,
        verbose_name=_("Status"),
        choices=Status.choices,
        default=Status.DRAFT,
    )
    end_date = models.DateTimeField(
        verbose_name=_("Time end of bid"),
    )

    def __str__(self) -> str:
        return self.name

    def clean_end_date(self):
        """Method for validate end date of lot."""
        if arrow.utcnow() >= self.end_date:
            raise ValidationError(
                _("End date can't be earlier that now"),
            )

    def clean_redemption_price(self):
        """Method for validate redemption price of lot."""
        if not self.redemption_price:
            return
        if self.redemption_price < self.start_price:
            raise ValidationError(
                _("Redemption price can not be less then start price"),
            )

    class Meta:
        verbose_name_plural = _("Lots")
        verbose_name = _("Lot")


class Category(BaseModel):
    """Model for Category."""

    name = models.CharField(
        max_length=32,
        verbose_name=_("Name"),
        unique=True,
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name_plural = _("Categories")
        verbose_name = _("Category")


class LotImage(BaseModel):
    """Model for lot image."""

    lot = models.ForeignKey(
        Lot,
        on_delete=models.CASCADE,
        verbose_name=_("Image of lot"),
        related_name="images",
    )
    image = models.ImageField(
        upload_to=settings.DEFAULT_MEDIA_PATH,
    )

    class Meta:
        verbose_name_plural = _("Images")
        verbose_name = _("Image")
