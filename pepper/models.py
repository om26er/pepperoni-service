from django.db import models


INT_DEFAULT = -1


class Review(models.Model):
    restaurant = models.ForeignKey('Restaurant', on_delete=models.CASCADE)
    reviewer_id = models.CharField(max_length=255, blank=False)
    review_stars = models.CharField(max_length=255, blank=False)
    review_text = models.CharField(max_length=2000, blank=True)

    class Meta:
        unique_together = ('restaurant', 'reviewer_id')


class Restaurant(models.Model):
    approved = models.BooleanField(default=True)
    business_type = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, unique=True, blank=False)
    name = models.CharField(max_length=255, blank=False)
    contact = models.CharField(max_length=255, blank=True)
    timings = models.CharField(max_length=255, blank=True)
    owner_name = models.CharField(max_length=255, blank=True)
    rating = models.FloatField(default=0)
    menu = models.FileField(blank=True)

    def __str__(self):
        return self.name

    @property
    def review_count(self):
        return len(Review.objects.filter(restaurant=self))
