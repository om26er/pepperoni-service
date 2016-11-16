from django.conf.urls import url

from pepper.views import RestaurantRegistration, RestaurantReview


urlpatterns = [
    url(r'^api/restaurants/register$', RestaurantRegistration.as_view()),
    url(r'^api/restaurants/review', RestaurantReview.as_view()),
]
