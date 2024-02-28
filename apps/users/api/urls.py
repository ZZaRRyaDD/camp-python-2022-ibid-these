from rest_framework.routers import DefaultRouter

from . import views

# router.register(r"users", UsersAPIView)
router = DefaultRouter()
router.register(r"", views.UsersViewSet, basename="user")
urlpatterns = router.urls
