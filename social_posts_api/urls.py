from django.urls import include, path
from rest_framework import routers

from social_posts_api.views import PostStatisticViewSet

router = routers.DefaultRouter()

router.register(r'posts_statistics', PostStatisticViewSet)

urlpatterns = [
    path('', include(router.urls))]
