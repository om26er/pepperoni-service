from rest_framework.generics import CreateAPIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from pepper.serializers import (
    RestaurantSerializer,
    ReviewValidationSerializer,
    RestaurantFilterSerializer,
)
from pepper.models import Restaurant, Review
from pepper.location import are_locations_within_radius


class RestaurantRegistration(CreateAPIView):
    serializer_class = RestaurantSerializer


class RestaurantFilter(APIView):
    serializer_class = RestaurantFilterSerializer

    def get_queryset(self):
        return [
            restaurant for restaurant in Restaurant.objects.all() if
            are_locations_within_radius(
                self.request.query_params.get('base_location'),
                restaurant.location, self.request.query_params.get('radius')
            )
        ]

    def get(self, *args, **kwargs):
        serializer = self.serializer_class(data=self.request.query_params)
        serializer.is_valid(raise_exception=True)
        restaurant_serializer = RestaurantSerializer(
            self.get_queryset(), many=True)
        return Response(restaurant_serializer.data, status=status.HTTP_200_OK)


class RestaurantReview(APIView):
    @staticmethod
    def is_restaurant_registered_for_location(location):
        try:
            Restaurant.objects.get(location=location)
        except Restaurant.DoesNotExist:
            return False
        else:
            return True

    @staticmethod
    def get_rating_mean_and_update(restaurant):
        pass

    @staticmethod
    def has_user_already_reviewed(reviewer_id, restaurant):
        try:
            Review.objects.get(restaurant=restaurant, reviewer_id=reviewer_id)
        except Review.DoesNotExist:
            return False
        else:
            return True

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
