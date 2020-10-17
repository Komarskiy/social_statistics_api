from datetime import datetime, timedelta

from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase

from social_posts_api.models import PostStatistic
from social_posts_api.serializers import PostStatisticSerializer


class CreatePostStatisticTest(APITestCase):
    """Test module for post statistic create."""

    def setUp(self):
        self.valid_payload = {
            'user_id': '1',
            'post_id': '2',
            'likes_count': 3
        }
        self.invalid_payload = {
            'user_id': '1',
            'post_id': '2',
            'likes_count': -100
        }
        self.url = reverse('poststatistic-list')

    def test_create_valid_post_statistic(self):
        response = self.client.post(self.url, self.valid_payload, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PostStatistic.objects.count(), 1)
        created_post_statistic = PostStatistic.objects.first()
        self.assertEqual(created_post_statistic.user_id, self.valid_payload['user_id'])
        self.assertEqual(created_post_statistic.post_id, self.valid_payload['post_id'])
        self.assertEqual(created_post_statistic.likes_count, self.valid_payload['likes_count'])

    def test_create_invalid_post_statistic(self):
        response = self.client.post(self.url, self.invalid_payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class GetLatestPostStatisticByPostTest(APITestCase):
    """Test module for get latest post statistic by post id."""

    def setUp(self):
        self.post_id = '1'

        # post_1_today may be last
        self.post_1_today = PostStatistic.objects.create(user_id='1', post_id=self.post_id, likes_count=10)

        self.post_1_yesterday = PostStatistic.objects.create(user_id='1', post_id=self.post_id, likes_count=5)
        self.post_1_yesterday.created_date = datetime.now(tz=timezone.utc) - timedelta(days=1)
        self.post_1_yesterday.save(update_fields=['created_date'])

        self.post_1_before_yesterday = PostStatistic.objects.create(user_id='1', post_id=self.post_id, likes_count=1)
        self.post_1_before_yesterday.created_date = datetime.now(tz=timezone.utc) - timedelta(days=2)
        self.post_1_before_yesterday.save(update_fields=['created_date'])

    def test_get_latest_post_statistic_by_post(self):
        url = reverse('poststatistic-last-post-stats-by-post', args=(self.post_id,))
        response = self.client.get(url)
        response_data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data['user_id'], self.post_1_today.user_id)
        self.assertEqual(response_data['post_id'], self.post_1_today.post_id)
        self.assertEqual(response_data['likes_count'], self.post_1_today.likes_count)

    def test_get_latest_post_statistic_by_post_not_found(self):
        url = reverse('poststatistic-last-post-stats-by-post', args=(1000,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class GetAllLatestPostStatisticByUserTest(APITestCase):
    """Test module for get all latest posts statistic by user id."""

    def setUp(self):
        self.post_1_id = '1'
        self.post_2_id = '2'
        self.user = '1'

        # post_1_today may be last
        self.post_1_today = PostStatistic.objects.create(user_id=self.user, post_id=self.post_1_id, likes_count=10)

        self.post_1_yesterday = PostStatistic.objects.create(user_id=self.user, post_id=self.post_1_id, likes_count=5)
        self.post_1_yesterday.created_date = datetime.now(tz=timezone.utc) - timedelta(days=1)
        self.post_1_yesterday.save(update_fields=['created_date'])

        # post_2_today may be last
        self.post_2_today = PostStatistic.objects.create(user_id=self.user, post_id=self.post_2_id, likes_count=20)

        self.post_2_yesterday = PostStatistic.objects.create(user_id=self.user, post_id=self.post_2_id, likes_count=1)
        self.post_2_yesterday.created_date = datetime.now(tz=timezone.utc) - timedelta(days=1)
        self.post_2_yesterday.save(update_fields=['created_date'])

    def test_get_all_latest_post_statistic_by_user(self):
        url = reverse('poststatistic-last-post-stats-by-user', args=(self.user,))
        response = self.client.get(url)
        response_data = response.json()

        correct_queryset = PostStatistic.objects.filter(pk__in=[self.post_1_today.pk, self.post_2_today.pk])
        serializer = PostStatisticSerializer(correct_queryset, many=True)
        self.assertEqual(response_data.get('results'), serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_latest_post_statistic_by_user_not_found(self):
        url = reverse('poststatistic-last-post-stats-by-user', args=(1000,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

