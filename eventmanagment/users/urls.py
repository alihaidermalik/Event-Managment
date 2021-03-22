from django.urls import path, include
from rest_framework import routers
from .views import UserViewSet
from django.views.decorators.csrf import csrf_exempt
from eventmanagment.users.views import (
    user_detail_view,
    user_redirect_view,
    user_update_view,
    UserViewSet,
)


app_name = "users"

router = routers.DefaultRouter()
router.register(r'signup', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path("~redirect/", view=user_redirect_view, name="redirect"),
    path("~update/", view=user_update_view, name="update"),
    path("<str:username>/", view=user_detail_view, name="detail"),
]
