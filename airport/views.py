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
    AirplaneListSerializer,
    AirplaneTypeSerializer,
    CrewSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    TicketSerializer,
    TicketListSerializer,
    TicketDetailSerializer,
    OrderSerializer,
    OrderListSerializer,
)


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = (IsAuthenticated,)


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer
    permission_classes = (IsAuthenticated,)


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.select_related("airplane_type")
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return AirplaneListSerializer
        return AirplaneSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer
    permission_classes = (IsAuthenticated,)


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.select_related("source", "destination")
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = (
        Flight.objects.select_related(
            "route__source",
            "route__destination",
            "airplane__airplane_type",
        )
        .prefetch_related("crew")
    )
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = self.queryset

        route_id = self.request.query_params.get("route")
        airplane_id = self.request.query_params.get("airplane")

        if route_id:
            queryset = queryset.filter(route_id=route_id)
        if airplane_id:
            queryset = queryset.filter(airplane_id=airplane_id)

        return queryset.distinct()

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.select_related(
        "flight__route__source",
        "flight__route__destination",
        "flight__airplane",
        "order",
    )
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == "list":
            return TicketListSerializer
        if self.action == "retrieve":
            return TicketDetailSerializer
        return TicketSerializer


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.prefetch_related(
        "tickets__flight__route__source",
        "tickets__flight__route__destination",
        "tickets__flight__airplane",
    )
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "list":
            return OrderListSerializer
        return OrderSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
