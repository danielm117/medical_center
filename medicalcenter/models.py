from django.db import models


class Result(models.Model):
    radius = models.CharField(max_length=20)
    initial_lat = models.FloatField()
    initial_lon = models.FloatField()
    index = models.IntegerField()


class Coordinate(models.Model):
    lat = models.FloatField()
    lon = models.FloatField()
    result = models.ForeignKey('Result', on_delete=models.CASCADE)

    def __str__(self):
        return '{}, {}'.format(self.lat, self.lon)
