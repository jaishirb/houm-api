from django.contrib.auth.models import User
from django.contrib.gis.db import models
from django_lifecycle import hook, BEFORE_UPDATE, AFTER_CREATE, AFTER_UPDATE

from apps.utils.models import BaseModel


class Property(BaseModel):
    name = models.CharField(max_length=200)
    description = models.TextField()
    coordinate = models.PointField(blank=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return str(self.uuid)

    class Meta:
        verbose_name = 'Property'
        verbose_name_plural = 'Properties'
        unique_together = ('coordinate', 'address')


class Houmer(User):
    last_location = models.PointField(blank=True, null=True)
    last_leaving_time = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Houmer'
        verbose_name_plural = 'Houmers'


class CompanyAgent(User):
    last_location = models.PointField(blank=True, null=True)

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'Company Agent'
        verbose_name_plural = 'Company Agents'


class HoumerHistoricalLocation(BaseModel):
    coordinate = models.PointField()
    datetime = models.DateTimeField(auto_now_add=True)
    houmer = models.ForeignKey(
        Houmer,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+'
    )
    velocity = models.FloatField(blank=True, null=True)

    def __str__(self):
        return str(self.uuid)

    @hook(AFTER_CREATE)
    def add_last_location(self):
        if self.houmer.last_location:
            point_a = self.houmer.last_location
            init_time = self.houmer.last_leaving_time
            point_b = self.coordinate
            end_time = self.datetime
            elapsed_time_hours = (end_time - init_time).seconds / 3600
            distance = point_a.distance(point_b)
            self.velocity = distance / elapsed_time_hours
        self.houmer.last_location = self.coordinate
        self.houmer.last_leaving_time = self.datetime

    class Meta:
        verbose_name = 'Houmer historical location'
        verbose_name_plural = 'Houmers historical locations'


class PropertyHomerVisit(BaseModel):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    houmer = models.ForeignKey(
        Houmer,
        blank=True,
        on_delete=models.CASCADE,
        related_name='+'
    )
    agent = models.ForeignKey(
        Houmer,
        on_delete=models.CASCADE,
        blank=True,
        related_name='+'
    )
    arrival_time = models.DateTimeField(auto_now_add=True)
    leaving_time = models.DateTimeField(blank=True, null=True)
    elapsed_time_seconds = models.PositiveIntegerField(blank=True, null=True)

    def __str__(self):
        return str(self.uuid)

    @hook(AFTER_UPDATE)
    def add_last_location_houmer(self):
        if self.leaving_time:
            self.houmer.last_location = self.property.coordinate
            self.houmer.last_leaving_time = self.leaving_time

    @hook(AFTER_CREATE)
    def add_last_location_agent(self):
        self.houmer.last_location = self.property.coordinate
        self.houmer.last_leaving_time = self.leaving_time

    @hook(BEFORE_UPDATE)
    def calculate_elapsed_time(self):
        if self.leaving_time:
            self.elapsed_time_seconds = (self.leaving_time - self.arrival_time).seconds
