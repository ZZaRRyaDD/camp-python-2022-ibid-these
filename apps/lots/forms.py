from django import forms
from django.utils.translation import gettext_lazy as _

from apps.lots import models


class LotCreateForm(forms.ModelForm):
    """Form for create lot."""

    class Meta:
        model = models.Lot
        fields = (
            "name",
            "description",
            "start_price",
            "bid_increment",
            "redemption_price",
            "status",
            "end_date",
            "category",
        )
        widgets = {
            "end_date": forms.TextInput(
                attrs={
                    "type": "datetime-local",
                },
            ),
        }


class LotImageForm(forms.ModelForm):
    """Form for one image of lot."""

    class Meta:
        model = models.LotImage
        fields = (
            "image",
        )


ImageLotFormSet = forms.inlineformset_factory(
    models.Lot,
    models.LotImage,
    form=LotImageForm,
    max_num=10,
    can_delete=True,
    extra=1,
)


class BidCreateForm(forms.ModelForm):
    """Form for create bid."""

    def __init__(self, lot, *args, **kwargs):
        """Override to store lot instance."""
        super().__init__(*args, **kwargs)
        self.lot = lot

    def clean_bid(self):
        """Validate price of bid more than start price or last bid."""
        last_bid = models.Bid.objects.filter(
            lot=self.lot,
        ).order_by("-created").first()
        min_expected_price = self.lot.start_price
        if last_bid:
            min_expected_price = last_bid.bid + self.lot.bid_increment
        if self.lot.start_price >= self.cleaned_data["bid"]:
            raise forms.ValidationError(
                _("Start price can not be more or equal than bid price"),
            )
        if self.cleaned_data["bid"] <= min_expected_price:
            raise forms.ValidationError(
                _(
                    "Current bid can not be less or equal, "
                    f"than previous bid ({min_expected_price})",
                ),
            )
        return self.cleaned_data["bid"]

    class Meta:
        model = models.Bid
        fields = (
            "bid",
        )
