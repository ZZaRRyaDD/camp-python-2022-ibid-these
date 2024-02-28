from django.urls import path

from . import views

app_name = "lots"
urlpatterns = [
    path("", views.LotListView.as_view(), name="list"),
    path("lot/create/", views.CreateLotView.as_view(), name="create"),
    path("lot/<int:pk>/update/", views.UpdateLotView.as_view(), name="update"),
    path("lot/<int:pk>/", views.DetailLotView.as_view(), name="details"),
    path("favorites/", views.FavoritesLotsView.as_view(), name="favorites"),
    path(
        "lot/<int:pk>/favorite/",
        views.FavoritesLotActionView.as_view(),
        name="action_favorites_lot",
    ),
]
