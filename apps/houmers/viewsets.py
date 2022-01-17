from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from apps.houmers.models import Property, Houmer, CompanyAgent, HoumerHistoricalLocation, PropertyHomerVisit
from apps.houmers.serializers import PropertySerializer, HoumerSerializer, CompanyAgentSerializer, \
    HoumerHistoricalLocationSerializer, PropertyHomerVisitSerializer


class PropertyViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating, listing, retrieving, deleting or
    updating properties

    This endpoint allows all CRUD operations and others from rest framework.

    You can see the full json request/response example going to 'http://localhost:4500'
    in swagger documentation.
    """
    model = Property
    queryset = model.objects.all()
    serializer_class = PropertySerializer


class HoumerViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating, listing, retrieving, deleting or
    updating houmers

    This endpoint allows all CRUD operations and others from rest framework.

    You can see the full json request/response example going to 'http://localhost:4500'
    in swagger documentation.
    """
    model = Houmer
    queryset = model.objects.all()
    serializer_class = HoumerSerializer


class CompanyAgentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating, listing, retrieving, deleting or
    updating company agents

    This endpoint allows all CRUD operations and others from rest framework.

    You can see the full json request/response example going to 'http://localhost:4500'
    in swagger documentation.
    """
    model = CompanyAgent
    queryset = model.objects.all()
    serializer_class = CompanyAgentSerializer


class HoumerHistoricalLocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint for creating historical records of houmers
    locations, by coordinates and datetime.
    This allows to the APP to send the coordinates of the houmer.

    This endpoint allows all CRUD operations and others from rest framework.

    Args (POST method):
        'point' -> str: '18.3432, 32.12344' (this is the coordinate)
    Returns:
        [json]: coordinate, datetime, houmer

    You can see the full json request/response example going to 'http://localhost:4500'
    in swagger documentation.
    """
    model = HoumerHistoricalLocation
    queryset = model.objects.all()
    serializer_class = HoumerHistoricalLocationSerializer

    @action(detail=False, methods=['GET'])
    def get_data_by_user_and_velocity(self, request):
        """
        API endpoint action for getting all of the moments in that houmers went to different
        properties with a velocity.

        You can see the full json request/response example going to 'http://localhost:4500'
        in swagger documentation.

        Args (GET method):
            'date' -> str: '2021-05-21' (this is the date for filtering)
            'velocity' -> float: this is the velocity limit in km/h
        Returns:
            [json]: visit, houmer, velocity
        """
        date_input = request.GET.get('date')
        velocity_limit = float(request.GET.get('velocity'))
        year, month, day = date_input.split('-')
        houmer = self.request.user
        moments = self.model.objects.filter(
            houmer_id=houmer.id,
            datetima__year=year,
            datetime__month=month,
            datetima__day=day,
            velocity__gt=velocity_limit
        )
        data = self.serializer_class(moments, many=True).data
        return Response(data, status=status.HTTP_200_OK)


class PropertyHomerVisitViewSet(viewsets.ModelViewSet):
    """
    API endpoint for getting all of the information including coordinates
    of the properties that houmers visited and how many time they used in each one
    and creating.

    This endpoint allows all CRUD operations and others from rest framework.

    You can see the full json request/response example going to 'http://localhost:4500'
    in swagger documentation.
    """
    model = PropertyHomerVisit
    queryset = model.objects.all()
    serializer_class = PropertyHomerVisitSerializer

    @action(detail=False, methods=['GET'])
    def get_data_by_user_and_day(self, request):
        """
        API endpoint action for getting all of the information including coordinates
        of the properties that houmers visited in a day and how many time they used in each one.

        You can see the full json request/response example going to 'http://localhost:4500'
        in swagger documentation.

        Args (GET method):
            'date' -> str: '2021-05-21' (this is the date for filtering)
        Returns:
            [json]: property, agent, arrival_time, leaving_time, elapsed_time (in seconds)
        """
        date_input = request.GET.get('date')
        year, month, day = date_input.split('-')
        houmer = self.request.user
        visits = self.model.objects.filter(
            houmer_id=houmer.id,
            arrival_time__year=year,
            arrival_time__month=month,
            arrival_time__day=day
        )
        data = self.serializer_class(visits, many=True).data
        return Response(data, status=status.HTTP_200_OK)
