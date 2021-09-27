from django.test import Client
from django.urls import reverse
from django.utils.http import urlencode

from tunes.tunes_combine import pull_tunes, combine_abc
from tunes.tests import factories

import pytest

def reverse_querystring(view, urlconf=None, args=None, kwargs=None, current_app=None, query_kwargs=None):
    '''Custom reverse to handle query strings.
    Usage:
        reverse('app.views.my_view', kwargs={'pk': 123}, query_kwargs={'search': 'Bob'})
    '''
    base_url = reverse(view, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    if query_kwargs:
        return '{}?{}'.format(base_url, urlencode(query_kwargs))
    return base_url

@pytest.mark.django_db
class TestDetailView:
    def test_shows_name(self):
        client = Client()
        
        # Create Tune and Get Id
        tune = factories.TuneFactory()
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
        tune1 = factories.TuneFactory()
        tune2 = factories.TuneFactory(name="Cooley", tune_info="Some info about tune")

        response = client.get(reverse("tunes:list"))

        assert response.status_code == 200, "View return 200 status code"
        assert tune1.name in response.content.decode(), "tune1.name shows in the list view"
        assert tune2.name in response.content.decode(), "tune2.name shows in the list view"

@pytest.mark.django_db
class TestABCCombineView:
    def test_show_combined_abc(self):
        """
        Test that tunes can be combined and shown on abc tune page
        """
        client = Client()

        # Create three tunes to go into database
        # with abc text
        tune1 = factories.TuneFactory(
            name = "Tune 1",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "reel"
            )
        )
        abctune1 = factories.ABCTuneFactory(
            tune = tune1
        )
        abctune1peice1 = factories.ABCTunePieceFactory(
            abc_tune = abctune1,
            part_order = 1,
            part_title = "Part 1",
            abc_piece = "|abcd|"    
        )
        abctune1peice2 = factories.ABCTunePieceFactory(
            abc_tune = abctune1,
            part_order = 2,
            part_title = "Part 2",
            abc_piece = "|efgA|"    
        )
        
        tune2 = factories.TuneFactory(
            name = "Tune 2",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "reel"
            )
        )
        abctune2 = factories.ABCTuneFactory(
            tune = tune2
        )
        abctune2peice1 = factories.ABCTunePieceFactory(
            abc_tune = abctune2,
            part_order = 1,
            part_title = "Part 1",
            abc_piece = "|ABCD|"    
        )
        abctune2peice2 = factories.ABCTunePieceFactory(
            abc_tune = abctune2,
            part_order = 2,
            part_title = "Part 2",
            abc_piece = "|EFGa|"    
        )

        tune3 = factories.TuneFactory(
            name = "Tune 3",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "reel"
            )
        )
        abctune3 = factories.ABCTuneFactory(
            tune = tune3
        )
        abctune3peice1 = factories.ABCTunePieceFactory(
            abc_tune = abctune3,
            part_order = 1,
            part_title = "Part 1",
            abc_piece = "|aaaa|"    
        )
        abctune3peice2 = factories.ABCTunePieceFactory(
            abc_tune = abctune3,
            part_order = 2,
            part_title = "Part 2",
            abc_piece = "|bbbb|"    
        )

        # Pass Query Parameters to URL
        response = client.get(reverse("tunes:abc_combine"))

        assert response.status_code == 200, "View returns 200 with no GET data"

        # Pass Query Parameters to URL
        response = client.get(
            reverse_querystring("tunes:abc_combine", query_kwargs={
                'num': 3, 
                'tune_type': 'reel'}
            )
        )

        assert response.status_code == 200, "View returns 200 status code"
        assert tune1.name in response.content.decode(), "Test that tune1.name in view"