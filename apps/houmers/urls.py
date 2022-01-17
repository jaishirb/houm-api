from django.urls import path, include
from rest_framework import routers

from apps.houmers import viewsets

router = routers.DefaultRouter()
router.register(r'properties', viewsets.PropertyViewSet, basename='properties')
router.register(r'houmers', viewsets.HoumerViewSet, basename='houmer')
router.register(r'agents', viewsets.CompanyAgentViewSet, basename='agent')
router.register(r'historical_locations', viewsets.HoumerHistoricalLocationViewSet, basename='historicals')
router.register(r'visits', viewsets.PropertyHomerVisitViewSet, basename='visits')
urlpatterns = [
    path(r'', include(router.urls))
]
