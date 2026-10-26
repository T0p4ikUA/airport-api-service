from django.conf import settings
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q, F
from rest_framework.exceptions import ValidationError


class Crew(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def __str__(self):
        return self.full_name


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_as_source",
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_as_destination",
    )
    distance = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ("source", "destination")
        constraints = [
            models.CheckConstraint(
                check=Q(distance__gt=0),
                name="distance_positive"
            ),
            models.CheckConstraint(
                check=~Q(source_id=F("destination_id")),
                name="source_not_destination"
            ),
        ]

    def clean(self):
        super().clean()
        if self.source == self.destination:
            raise ValidationError(
                "Airport of destination and source cannot be the same"
            )

    def __str__(self):
        return (f"{self.source} -> {self.destination}"
                f" distance: {self.distance}km")


class AirplaneType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.IntegerField(validators=[MinValueValidator(1)])
    seats_in_row = models.IntegerField(validators=[MinValueValidator(1)])
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(rows__gt=0),
                name="rows_positive"
            ),
            models.CheckConstraint(
                check=Q(seats_in_row__gt=0),
                name="seats_in_row_positive"
            ),
        ]

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name} (rows: {self.rows}, seats: {self.seats_in_row})"


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights",
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights",
    )
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    crew = models.ManyToManyField(
        Crew,
        related_name="flights",
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                check=Q(arrival_time__gt=F("departure_time")),
                name="arrival_after_departure"
            ),
        ]

    def clean(self):
        super().clean()
        if self.arrival_time <= self.departure_time:
            raise ValidationError({
                "arrival_time": (
                    "arrival_time must be later "
                    "than departure_time"
                )
            })

    def __str__(self):
        return f"{self.route} | departure: {self.departure_time}"


class Order(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"Order #{self.id} by {self.user}"


class Ticket(models.Model):
    row = models.IntegerField(validators=[MinValueValidator(1)])
    seat = models.IntegerField(validators=[MinValueValidator(1)])
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets",
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets",
        null=True,
        blank=True,
    )

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        for tkt_value, tkt_range, error_msg in [
            (row,
             airplane.rows,
             f"Row number must be between 1 and {airplane.rows}"),
            (
                seat,
                airplane.seats_in_row,
                f"Seat number must be between 1 and {airplane.seats_in_row}",
            ),
        ]:
            if not (1 <= tkt_value <= tkt_range):
                raise error_to_raise(
                    {"row" if tkt_value == row else "seat": error_msg}
                )

    def clean(self):
        super().clean()
        Ticket.validate_ticket(
            self.row, self.seat, self.flight.airplane, ValidationError
        )

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)

    class Meta:
        unique_together = ("flight", "row", "seat")

    def __str__(self):
        return f"Flight: {self.flight} (Row: {self.row}, Seat: {self.seat})"
