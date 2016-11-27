from django.conf.urls import url

from pepper.views import (
    RestaurantRegistration,
    RestaurantReview,
    RestaurantFilter,
)


urlpatterns = [
    url(r'^api/restaurants/register$', RestaurantRegistration.as_view()),
    url(r'^api/restaurants/filter$', RestaurantFilter.as_view()),
    url(r'^api/restaurants/review$', RestaurantReview.as_view()),
]
