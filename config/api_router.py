from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from apps.courses.views import CourseViewSet
from apps.users.views import UserViewSet

router = DefaultRouter() if settings.DEBUG else SimpleRouter()
router.register("users", UserViewSet)
router.register("courses", CourseViewSet)

app_name = "api"
urlpatterns = router.urls
