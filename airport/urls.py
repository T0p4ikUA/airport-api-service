from django.urls import path, include
from rest_framework import routers

from airport.views import (
    AirportViewSet,
    AirplaneViewSet,
    AirplaneTypeViewSet,
    CrewViewSet,
    RouteViewSet,
    FlightViewSet,
    OrderViewSet,
    TicketViewSet,
)

router = routers.DefaultRouter()

router.register("airports", AirportViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("crew", CrewViewSet)
router.register("routes", RouteViewSet)
router.register("flights", FlightViewSet)
router.register("orders", OrderViewSet)
router.register("tickets", TicketViewSet)

app_name = "airport"

urlpatterns = [
    path("", include(router.urls)),
]