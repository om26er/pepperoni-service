from django.conf.urls import include, url
from django.contrib import admin

from pepper import urls as pepper_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^', include(pepper_urls))
]
