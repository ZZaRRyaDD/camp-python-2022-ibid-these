from django.contrib import admin

from . import models


@admin.register(models.Lot)
class LotAdmin(admin.ModelAdmin):
    """Class representation of Lot model in admin panel."""

    autocomplete_fields = (
        "interest_users",
        "category",
        "user",
    )
    search_fields = (
        "name",
    )
    list_display = (
        "id",
        "name",
        "description",
        "start_price",
        "bid_increment",
        "redemption_price",
        "status",
        "end_date",
    )
    list_filter = (
        "category",
    )
    fieldsets = (
        ("Base info", {
            "fields": (
                "name",
                "description",
                "start_price",
                "bid_increment",
                "redemption_price",
                "status",
                "end_date",
                "category",
            ),
        }),
    )


@admin.register(models.LotImage)
class LotImageAdmin(admin.ModelAdmin):
    """Class representation of LotImage model in admin panel."""

    autocomplete_fields = (
        "lot",
    )
    list_display = (
        "id",
        "image",
    )


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """Class representation of Category model in admin panel."""

    search_fields = (
        "name",
    )
    list_display = (
        "id",
        "name",
    )


@admin.register(models.Bid)
class BidAdmin(admin.ModelAdmin):
    """Class representation of Bid model in admin panel."""

    autocomplete_fields = (
        "lot",
        "user",
    )
    list_display = (
        "id",
        "bid",
        "created",
    )
