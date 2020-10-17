from rest_framework import serializers

from social_posts_api.models import PostStatistic


class PostStatisticSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostStatistic
        fields = ['user_id', 'post_id', 'likes_count']
