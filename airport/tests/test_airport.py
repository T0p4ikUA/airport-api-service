from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from airport.models import (
    Airport,
    AirplaneType,
    Airplane,
    Crew,
    Route,
    Flight,
    Order,
    Ticket,
)
from airport.serializers import (
    AirportSerializer,
    AirplaneTypeSerializer,
    CrewSerializer,
    RouteListSerializer,
    AirplaneSerializer,
    AirplaneListSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    TicketListSerializer,
)

AIRPORT_URL = reverse("airport:airport-list")
AIRPLANETYPE_URL = reverse("airport:airplanetype-list")
AIRPLANE_URL = reverse("airport:airplane-list")
CREW_URL = reverse("airport:crew-list")
ROUTE_URL = reverse("airport:route-list")
FLIGHT_URL = reverse("airport:flight-list")
ORDER_URL = reverse("airport:order-list")
TICKET_URL = reverse("airport:ticket-list")


def detail_url(name, obj_id):
    return reverse(f"airport:{name}-detail", args=(obj_id,))


def sample_airport(**params):
    defaults = {
        "name": "Boryspil",
        "closest_big_city": "Kyiv",
    }
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_airplane_type(**params):
    name = params.get("name", "Boeing 737")
    defaults = {
        "name": name,
    }
    defaults.update(params)
    return AirplaneType.objects.get_or_create(**defaults)[0]


def sample_crew(**params):
    defaults = {
        "first_name": "John",
        "last_name": "Doe",
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)


def sample_route(**params):
    source = sample_airport(name="Lviv", closest_big_city="Lviv")
    destination = sample_airport(name="Kyiv", closest_big_city="Kyiv")
    defaults = {
        "source": source,
        "destination": destination,
        "distance": 500,
    }
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_airplane(**params):
    airplane_type = sample_airplane_type()
    defaults = {
        "name": "Boeing 737-800",
        "rows": 30,
        "seats_in_row": 6,
        "airplane_type": airplane_type,
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def sample_flight(**params):
    route = sample_route()
    airplane = sample_airplane()
    defaults = {
        "route": route,
        "airplane": airplane,
        "departure_time": "2026-10-25T10:00:00Z",
        "arrival_time": "2026-10-25T12:00:00Z",
    }
    defaults.update(params)
    return Flight.objects.create(**defaults)


class UnauthenticatedAirportApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(AIRPLANE_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAirportAndExtrasApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_airports_list(self):
        sample_airport()
        res = self.client.get(AIRPORT_URL)
        airports = Airport.objects.all()
        serializer = AirportSerializer(airports, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_airplane_types_list(self):
        sample_airplane_type()
        res = self.client.get(AIRPLANETYPE_URL)
        types = AirplaneType.objects.all()
        serializer = AirplaneTypeSerializer(types, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_crew_list(self):
        sample_crew()
        res = self.client.get(CREW_URL)
        crew = Crew.objects.all()
        serializer = CrewSerializer(crew, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_routes_list(self):
        sample_route()
        res = self.client.get(ROUTE_URL)
        routes = Route.objects.select_related("source", "destination")
        serializer = RouteListSerializer(routes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_tickets_list(self):
        flight = sample_flight()
        order = Order.objects.create(user=self.user)
        Ticket.objects.create(row=1, seat=1, flight=flight, order=order)

        res = self.client.get(TICKET_URL)
        tickets = Ticket.objects.select_related(
            "flight__route__source", "flight__route__destination", "flight__airplane", "order"
        )
        serializer = TicketListSerializer(tickets, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class AuthenticatedAirplaneApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_airplanes_list(self):
        sample_airplane()
        res = self.client.get(AIRPLANE_URL)
        airplanes = Airplane.objects.select_related("airplane_type")
        serializer = AirplaneListSerializer(airplanes, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_airplane_detail(self):
        airplane = sample_airplane()
        url = detail_url("airplane", airplane.id)

        res = self.client.get(url)
        serializer = AirplaneSerializer(airplane)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class FlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_flights_list(self):
        sample_flight()
        res = self.client.get(FLIGHT_URL)
        flights = Flight.objects.select_related(
            "route__source", "route__destination", "airplane__airplane_type"
        ).prefetch_related("crew")
        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_flights_by_route(self):
        flight1 = sample_flight()
        route2 = sample_route()
        route2.source.name = "Odesa"
        route2.source.save()
        flight2 = sample_flight(route=route2)

        res = self.client.get(FLIGHT_URL, {"route": flight1.route.id})

        serializer1 = FlightListSerializer(flight1)
        serializer2 = FlightListSerializer(flight2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_flight_detail(self):
        flight = sample_flight()
        url = detail_url("flight", flight.id)

        res = self.client.get(url)
        serializer = FlightDetailSerializer(flight)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)


class OrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.test", password="testpassword"
        )
        self.client.force_authenticate(self.user)

    def test_create_order_with_tickets(self):
        flight = sample_flight()
        payload = {
            "tickets": [
                {"row": 1, "seat": 1, "flight": flight.id},
                {"row": 1, "seat": 2, "flight": flight.id},
            ]
        }
        res = self.client.post(ORDER_URL, payload, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        order = Order.objects.get(id=res.data["id"])
        self.assertEqual(order.user, self.user)
        self.assertEqual(order.tickets.count(), 2)

    def test_ticket_validation_out_of_range(self):
        flight = sample_flight()
        payload = {
            "tickets": [
                {"row": 35, "seat": 1, "flight": flight.id},
            ]
        }
        res = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
