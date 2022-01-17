from django.contrib.gis.geos import Point
from rest_framework import serializers

from apps.houmers import models
from apps.utils.serializers import CustomSerializer


class PropertySerializer(CustomSerializer):
    """
    The implementation of the custom serializer it used for writing shorter serializers and
    more practical ones
    """
    class Meta:
        model = models.Property
        extra_kwargs = {'coordinate': {'required': False}}
        validators = []
        exclude = ('deleted',)

    def create(self, validated_data):
        data = self.context.get('request').data
        if data.get('point'):
            point = list(map(float, data.pop('point').strip().split(',')))
            coordinate = Point(point[0], point[1], srid=4326)
            data.update({
                'coordinate': coordinate
            })
        return super().create(data)


class HoumerSerializer(CustomSerializer):
    class Meta:
        model = models.Houmer
        exclude = ('password',)

    def update(self, instance, validated_data):
        """
        mapping the string with coordinate to Point object
        due to it's not json serializable at the beginning
        """
        data = self.context.get('request').data
        if data.get('point'):
            point = list(map(float, data.pop('point').strip().split(',')))
            coordinate = Point(point[0], point[1], srid=4326)
            instance.last_location = coordinate
        instance.save()
        return instance


class CompanyAgentSerializer(CustomSerializer):
    class Meta:
        model = models.CompanyAgent
        exclude = ('password', )

    def update(self, instance, validated_data):
        data = self.context.get('request').data
        if data.get('point'):
            point = list(map(float, data.pop('point').strip().split(',')))
            coordinate = Point(point[0], point[1], srid=4326)
            instance.last_location = coordinate
        instance.save()
        return instance


class HoumerHistoricalLocationSerializer(CustomSerializer):
    class Meta:
        model = models.HoumerHistoricalLocation
        exclude = ('deleted', 'houmer')
        depth = 1
        extra_kwargs = {'coordinate': {'required': False}}

    def create(self, validated_data):
        """
        mapping the user that makes the request and assign it to
        the data for creating the record in model
        """
        request = self.context.get('request')
        data = request.data
        if not request.user.is_anonymous:
            data.update({
                'houmer_id': self.context.get('request').user.id
            })
            if data.get('point'):
                point = list(map(float, data.pop('point').strip().split(',')))
                coordinate = Point(point[0], point[1], srid=4326)
                data.update({
                    'coordinate': coordinate
                })
                return super().create(data)
            raise serializers.ValidationError({'error': 'point attr is required.'})
        raise serializers.ValidationError({'error': 'User must be authenticated'})


class PropertyHomerVisitSerializer(CustomSerializer):
    class Meta:
        model = models.PropertyHomerVisit
        exclude = ('deleted', 'houmer')
        depth = 1

    def create(self, validated_data):
        request = self.context.get('request')
        data = request.data
        if not request.user.is_anonymous:
            data.update({
                'houmer_id': self.context.get('request').user.id
            })
            return super().create(data)
        raise serializers.ValidationError({'error': 'User must be authenticated'})
