from rest_framework import serializers
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


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type_name = serializers.SlugRelatedField(
        read_only=True,
        slug_field="name",
        source="airplane_type",
    )
    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "capacity",
            "airplane_type",
            "airplane_type_name",
        )


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class RouteSerializer(serializers.ModelSerializer):
    source = AirportSerializer(read_only=True)
    source_id = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(),
        source="source",
        write_only=True,
    )
    destination = AirportSerializer(read_only=True)
    destination_id = serializers.PrimaryKeyRelatedField(
        queryset=Airport.objects.all(),
        source="destination",
        write_only=True,
    )

    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "source_id",
            "destination",
            "destination_id",
            "distance",
        )


class FlightSerializer(serializers.ModelSerializer):
    route = RouteSerializer(read_only=True)
    route_id = serializers.PrimaryKeyRelatedField(
        queryset=Route.objects.all(),
        source="route",
        write_only=True,
    )
    airplane = AirplaneSerializer(read_only=True)
    airplane_id = serializers.PrimaryKeyRelatedField(
        queryset=Airplane.objects.all(),
        source="airplane",
        write_only=True,
    )
    crew = CrewSerializer(read_only=True, many=True)
    crew_ids = serializers.PrimaryKeyRelatedField(
        queryset=Crew.objects.all(),
        source="crew",
        write_only=True,
        many=True,
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "route_id",
            "airplane",
            "airplane_id",
            "departure_time",
            "arrival_time",
            "crew",
            "crew_ids",
        )


class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight")


class TicketListSerializer(TicketSerializer):
    flight = FlightSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, allow_empty=False)

    class Meta:
        model = Order
        fields = ("id", "tickets", "created_at")

    def create(self, validated_data):
        tickets_data = validated_data.pop("tickets")
        order = Order.objects.create(**validated_data)
        for ticket in tickets_data:
            Ticket.objects.create(
                order=order,
                **ticket,
            )
        return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)
