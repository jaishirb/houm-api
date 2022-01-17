from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from apps.houmers import models
from apps.houmers.forms import HoumerForm, CompanyAgentForm


@admin.register(models.Property)
class PropertyAdmin(LeafletGeoAdmin):
    list_display = (
        'uuid',
        'name',
        'description',
        'coordinate',
        'address'
    )
    search_fields = (
        'name',
        'id',
        'address'
    )


@admin.register(models.Houmer)
class HoumerAdmin(LeafletGeoAdmin):
    form = HoumerForm
    list_display = (
        'username',
        'email',
        'is_active',
        'last_location',
        'last_leaving_time'
    )
    search_fields = (
        'username',
        'email',
        'id'
    )
    list_filter = (
        'is_active',
    )


@admin.register(models.CompanyAgent)
class CompanyAgentAdmin(LeafletGeoAdmin):
    form = CompanyAgentForm
    list_display = (
        'username',
        'email',
        'is_active',
        'last_location',
    )
    search_fields = (
        'username',
        'email',
        'id'
    )
    list_filter = (
        'is_active',
    )


@admin.register(models.HoumerHistoricalLocation)
class HoumerHistoricalLocationAdmin(LeafletGeoAdmin):
    list_display = (
        'uuid',
        'coordinate',
        'datetime',
        'houmer'
    )
    search_fields = (
        'houmer__username',
        'id'
    )
    list_filter = (
        'datetime',
    )


@admin.register(models.PropertyHomerVisit)
class PropertyHomerVisitAdmin(LeafletGeoAdmin):
    list_display = (
        'uuid',
        'property',
        'houmer',
        'agent',
        'arrival_time',
        'leaving_time',
        'elapsed_time_seconds'
    )
    search_fields = (
        'houmer__username',
        'agent__username',
        'id'
    )
