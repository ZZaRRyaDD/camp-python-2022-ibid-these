from django.core import validators
from django.db import models


class PriceField(models.DecimalField):
    """Base field to use for prices."""

    def __init__(self, **kwargs):
        """Custom field for price."""

        defaults = dict(
            decimal_places=2,
            max_digits=11,
        )
        defaults.update(**kwargs)
        super().__init__(**defaults)
        self.validators.append(validators.MinValueValidator(0))
