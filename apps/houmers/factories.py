import factory
from django.contrib.auth.hashers import make_password
from django.contrib.gis.geos import Point

from apps.houmers.models import Houmer, CompanyAgent, Property
from apps.utils.tests import faker


class HoumerFactory(factory.django.DjangoModelFactory):
    """
    Factories Design pattern implemented for using in tests
    with fakers for generating random data, in this way we can scale up
    our tests.
    this allow us to be more efficient writing our tests.
    """
    class Meta:
        model = Houmer

    username = factory.LazyAttribute(lambda _: faker.unique.name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    password = factory.LazyAttribute(lambda _: make_password(faker.word))


class AgentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CompanyAgent

    username = factory.LazyAttribute(lambda _: faker.unique.name())
    email = factory.LazyAttribute(lambda _: faker.unique.email())
    password = factory.LazyAttribute(lambda _: make_password(faker.word))


class PropertyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Property

    name = factory.LazyAttribute(lambda _: faker.unique.name())
    description = factory.LazyAttribute(lambda _: faker.text())
    coordinate = factory.LazyAttribute(lambda _: Point(faker.pyfloat(), faker.pyfloat()))
    address = factory.LazyAttribute(lambda _: faker.address())

