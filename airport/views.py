from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from airport.models import (
    Airport,
    Airplane,
    AirplaneType,
    Crew,
    Flight,
    Order,
    Route,
    Ticket,
)
from airport.serializers import (
AirportSerializer,
AirplaneSerializer,
AirplaneTypeSerializer,
CrewSerializer,
FlightSerializer,
OrderSerializer,
OrderListSerializer,
RouteSerializer,
TicketSerializer,
TicketListSerializer,
)

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    serializer_class = AirplaneSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = (Flight.objects.select_related(
        "route__source",
        "route__destination",
        "airplane__airplane_type",
    )
                .prefetch_related("crew"))
    serializer_class = FlightSerializer


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    serializer_class = RouteSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related("user")
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related("flight", "order")
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        return TicketSerializer
