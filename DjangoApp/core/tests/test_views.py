# core/test/test_views.py

from django.test import Client
from django.urls import reverse

class TestHomeView:
    def test_response(self):
        client = Client()
        response = client.get(reverse("home"))
        
        assert response.status_code == 200, "Home View returns 200 status"
        assert "<title>40SessionTunes</title>" in \
            response.content.decode(), "Home View renders with correct title"

class TestMidiExample1View:
    def test_response(self):
        client = Client()
        response = client.get(reverse("midiexample_1"))
        
        assert response.status_code == 200, "Midi Example 1 View returns 200 status"

class TestMidiExample2View:
    def test_response(self):
        client = Client()
        response = client.get(reverse("midiexample_2"))
        
        assert response.status_code == 200, "Midi Example 2 View returns 200 status"