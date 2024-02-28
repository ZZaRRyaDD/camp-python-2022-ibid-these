from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.core.fields import PriceField
from apps.core.models import BaseModel


class Bid(BaseModel):
    """Model for bid per lot."""

    bid = PriceField(
        verbose_name=_("Bid"),
    )
    lot = models.ForeignKey(
        "lots.Lot",
        on_delete=models.CASCADE,
        related_name="bids",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="bids",
    )

    def __str__(self) -> str:
        return f"Bid {self.bid} of {self.lot.name} lot"

    class Meta:
        verbose_name_plural = _("Bids")
        verbose_name = _("Bid")
