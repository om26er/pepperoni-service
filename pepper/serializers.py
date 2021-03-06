from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from pepper.models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    approved = serializers.BooleanField(read_only=True)
    name = serializers.CharField(required=True)
    location = serializers.CharField(
        required=True,
        validators=[UniqueValidator(queryset=Restaurant.objects.all())]
    )
    contact = serializers.CharField(required=True)
    timings = serializers.CharField(required=True)
    owner_name = serializers.CharField(required=True)
    business_type = serializers.CharField(required=True)
    rating = serializers.FloatField(required=False)
    menu = serializers.FileField(required=False)
    review_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Restaurant
        fields = '__all__'

    def create(self, validated_data):
        validated_data.update({'approved': False})
        return super().create(validated_data)


class ReviewValidationSerializer(serializers.Serializer):
    review_stars = serializers.CharField(required=True)
    location = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    review_text = serializers.CharField(required=False)
    reviewer_id = serializers.CharField(required=True)


class RestaurantFilterSerializer(serializers.Serializer):
    radius = serializers.IntegerField(required=True)
    base_location = serializers.CharField(required=True)
