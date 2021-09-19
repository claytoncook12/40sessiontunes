from django.test import Client
from django.urls import reverse

from tunes.tests.factories import TuneFactory

import pytest

@pytest.mark.django_db
class TestDetailView:
    def test_shows_name(self):
        client = Client()
        
        # Create Tune and Get Id
        tune = TuneFactory()
        id  = tune.id

        # Get detail view of tune created above
        response = client.get(reverse("tunes:detail", args=(id,)))

        assert response.status_code == 200, "View returns 200 status code"
        assert tune.name in response.content.decode(), "The tunes.detail view shows the tune.name"

@pytest.mark.django_db
class TestListView:
    def test_shows_list(self):
        client = Client()

        # Create a Few Tune for Database
        tune1 = TuneFactory()
        tune2 = TuneFactory(name="Cooley", tune_info="Some info about tune")

        response = client.get(reverse("tunes:list"))

        assert response.status_code == 200, "View return 200 status code"
        assert tune1.name in response.content.decode(), "tune1.name shows in the list view"
        assert tune2.name in response.content.decode(), "tune2.name shows in the list view"