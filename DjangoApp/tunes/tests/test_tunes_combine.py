# test_tunes_combine.py

from tunes.tests import factories
from tunes import models

import pytest

from tunes import tunes_combine

@pytest.mark.django_db
class TestMakeSet:
    def test_pull_tunes(self):
        # Create 5 tunes for database
        tune1 = factories.TuneFactory(
            name = "Tune 1",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "reel"
            )
        )
        tune2 = factories.TuneFactory(
            name = "Tune 2",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "reel"
            )
        )
        tune3 = factories.TuneFactory(
            name = "Tune 3",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "reel"
            )
        )
        tune4 = factories.TuneFactory(
            name = "Tune 4",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "jig"
            )
        )
        tune5 = factories.TuneFactory(
            name = "Tune 5",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "jig"
            )
        )

        # Check that queryset returns correct objects
        qs = tunes_combine.pull_tunes(num=3,tune_type="reel")
        assert len(qs) == 3, "Should pull only 3 of 5 tunes that are reels"
        assert (tune1 in qs) == True, "Should contain tune1"
        assert (tune2 in qs) == True, "Should contain tune2"
        assert (tune3 in qs) == True, "Should contain tune3"
        assert (tune4 in qs) == False, "Should not contain tune4"
        assert (tune5 in qs) == False, "Should not contain tune5"
        
        # Check that queryset returns correct objects
        qs = tunes_combine.pull_tunes(num=2,tune_type="jig")
        assert len(qs) == 2, "Should pull only 2 of 5 tunes that are jigs"
        assert (tune1 in qs) == False, "Should not contain tune1"
        assert (tune2 in qs) == False, "Should not contain tune2"
        assert (tune3 in qs) == False, "Should not contain tune3"
        assert (tune4 in qs) == True, "Should contain tune4"
        assert (tune5 in qs) == True, "Should contain tune5"