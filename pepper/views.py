from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pepper.serializers import (
    RestaurantSerializer,
    ReviewValidationSerializer,
)
from pepper.models import Restaurant, Review


class RestaurantRegistration(CreateAPIView):
    serializer_class = RestaurantSerializer


class RestaurantReview(APIView):
    @staticmethod
    def is_restaurant_registered_for_location(location):
        try:
            Restaurant.objects.get(location=location)
            return True
        except Restaurant.DoesNotExist:
            return False

    @staticmethod
    def get_rating_mean_and_update(restaurant):
        pass

    @staticmethod
    def has_user_already_reviewed(reviewer_id, restaurant):
        try:
            Review.objects.get(restaurant=restaurant, reviewer_id=reviewer_id)
            return True
        except Review.DoesNotExist:
            return False

    def post(self, *args, **kwargs):
        validator = ReviewValidationSerializer(data=self.request.data)
        validator.is_valid(raise_exception=True)
        data = self.request.data
        if self.is_restaurant_registered_for_location(data['location']):
            restaurant = Restaurant.objects.get(location=data['location'])
        else:
            d = data.copy()
            d.pop('reviewer_id')
            d.pop('review_stars')
            restaurant = Restaurant.objects.create(**d)
        if self.has_user_already_reviewed(data['reviewer_id'], restaurant):
            return Response(
                data={'message': 'REVIEWED_ALREADY'},
                status=status.HTTP_409_CONFLICT
            )
        data.pop('location')
        data.pop('name')
        Review.objects.create(restaurant=restaurant, **data)
        return Response(status=status.HTTP_201_CREATED)
