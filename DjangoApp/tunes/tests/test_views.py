from django.test import Client
from django.urls import reverse

from tunes.tests.factories import TuneFactory

import pytest

@pytest.mark.django_db
class TestDetailView:
    def test_shows_name(self):
        """ The tunes.detail view shows the tune.name  """
        client = Client()
        
        # Create Tune and Get Id
        tune = TuneFactory()
        id  = tune.id

        # Get detail view of tune created above
        response = client.get(reverse("tunes:detail", args=(id,)))

        assert response.status_code == 200
        assert tune.name in response.content.decode()