from datetime import datetime, timedelta

from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.mixins import CreateModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from social_posts_api.models import PostStatistic
from social_posts_api.serializers import PostStatisticSerializer


# Default pagination class
class DefaultPagination(PageNumberPagination):
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 20


class PostStatisticViewSet(CreateModelMixin, viewsets.GenericViewSet):
    queryset = PostStatistic.objects.all()
    serializer_class = PostStatisticSerializer
    pagination_class = DefaultPagination

    @action(detail=False, methods=['GET'], url_path='posts/(?P<post_id>\d+)/latest', url_name='last-post-stats-by-post')
    def latest_by_post(self, request, post_id):
        """
        Return latest​ statistics for a specific post id
        """
        # get latest post statistic
        post_statistic = (
            PostStatistic
            .objects
            .filter(post_id=post_id)
            .order_by('-created_date')
            .values('user_id', 'post_id', 'likes_count')
            .first()
        )
        if post_statistic:
            serializer = self.get_serializer(post_statistic)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['GET'], url_path='users/(?P<user_id>\d+)/latest', url_name='last-post-stats-by-user')
    def latest_by_user(self, request, user_id):
        """
        Return latest​ statistics for all posts of a specific user id
        """
        # get latest post statistics for each user posts
        post_statistics = (
            PostStatistic
            .objects
            .filter(user_id=user_id)
            .order_by('post_id', '-created_date')
            .values('user_id', 'post_id', 'likes_count')
            .distinct('post_id')
        )
        if post_statistics:
            # response pagination
            page = self.paginate_queryset(post_statistics)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = self.get_serializer(post_statistics, many=True)
            return Response(serializer.data)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['GET'], url_path='users/(?P<user_id>\d+)/average', detail=False)
    def average(self, request, user_id):
        """
        Return average number of likes per day for a specific user id for the last 30 days.
        """
        # get last day from last month
        last_month = datetime.now() - timedelta(days=30)

        # get latest post statistics for each user posts
        post_statistics = (
            PostStatistic
            .objects
            .filter(user_id=user_id, created_date__gt=last_month)
            .values_list('pk', flat=True)
            .order_by('post_id', '-created_date')
            .distinct('post_id')
        )

        if post_statistics:
            # Get average number of likes per day for a specific user id for the last 30 days
            likes_per_day = (
                 PostStatistic.objects
                 .filter(pk__in=post_statistics)
                 .aggregate(likes_per_day=Sum('likes_count') / 30)
            )
            data = {
                'user_id': int(user_id),
                'likes_per_day': likes_per_day.get('likes_per_day')
            }
            return Response(data)

        return Response(status=status.HTTP_404_NOT_FOUND)
