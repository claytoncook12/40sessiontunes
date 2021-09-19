# core/test/test_views.py

from django.test import Client
from django.urls import reverse

class TestHomeView:
    def test_response(self):
        client = Client()
        response = client.get(reverse("home"))
        
        assert response.status_code == 200, "Home View returns 200 status"