from django.db import models


INT_DEFAULT = -1


class Review(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    reviewer_id = models.CharField(max_length=255, blank=False, unique=True)
    review_stars = models.IntegerField(blank=False)
    review_text = models.CharField(max_length=2000, blank=True)


class Restaurant(models.Model):
    approved = models.BooleanField(default=True)
    location = models.CharField(max_length=255, unique=True, blank=False)
    name = models.CharField(max_length=255, blank=False)
    contact = models.CharField(max_length=255, blank=True)
    opening_time = models.CharField(max_length=255, blank=True)
    closing_time = models.CharField(max_length=255, blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    rating = models.IntegerField(default=0)
    menu = models.FileField(blank=True)

    def __str__(self):
        return self.name
