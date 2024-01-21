from rest_framework import serializers
from .models import Content, Rating


class ContentSerializer(serializers.ModelSerializer):
    ratings_count = serializers.SerializerMethodField()
    ratings_average = serializers.SerializerMethodField()
    my_rating = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ("title", "text", "ratings_count", "ratings_average", "my_rating")

    def get_ratings_count(self, obj: Content):
        return obj.ratings.count()

    def get_ratings_average(self, obj: Content):
        if obj.ratings.count() == 0:
            return 0
        return sum(obj.ratings.values_list("rating", flat=True)) / obj.ratings.count()

    def get_my_rating(self, obj: Content):
        user = self.context.get('user')
        rating = obj.ratings.filter(user=user).first()
        if rating:
            return rating.rating
        return None


class RatingSerializer(serializers.Serializer):
    rating = serializers.IntegerField()
