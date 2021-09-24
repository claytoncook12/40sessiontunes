# test_tunes_combine.py

from tunes.tests import factories
from tunes import models

import pytest

from tunes import tunes_combine

@pytest.mark.django_db
class Test:
    @pytest.fixture
    def setup_data(self):
        # Create 5 tunes, abctune, and abc for database
        self.tune1 = factories.TuneFactory(
            name = "Tune 1",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "reel"
            )
        )
        self.abctune1 = factories.ABCTuneFactory(
            tune = self.tune1
        )
        self.abctune1peice1 = factories.ABCTunePieceFactory(
            abc_tune = self.abctune1,
            part_order = 1,
            part_title = "Part 1",
            abc_piece = "|abcd|"    
        )
        self.abctune1peice2 = factories.ABCTunePieceFactory(
            abc_tune = self.abctune1,
            part_order = 2,
            part_title = "Part 2",
            abc_piece = "|efga|"    
        )
        
        self.tune2 = factories.TuneFactory(
            name = "Tune 2",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "reel"
            )
        )
        self.tune3 = factories.TuneFactory(
            name = "Tune 3",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "reel"
            )
        )
        self.tune4 = factories.TuneFactory(
            name = "Tune 4",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "jig"
            )
        )
        self.tune5 = factories.TuneFactory(
            name = "Tune 5",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "jig"
            )
        )

    def test_pull_tunes(self, setup_data):
        # Check that queryset returns correct objects
        qs = tunes_combine.pull_tunes(num=3,tune_type="reel")
        assert len(qs) == 3, "Should pull only 3 of 5 tunes that are reels"
        assert (self.tune1 in qs) == True, "Should contain tune1"
        assert (self.tune2 in qs) == True, "Should contain tune2"
        assert (self.tune3 in qs) == True, "Should contain tune3"
        assert (self.tune4 in qs) == False, "Should not contain tune4"
        assert (self.tune5 in qs) == False, "Should not contain tune5"
        
        # Check that queryset returns correct objects
        qs = tunes_combine.pull_tunes(num=2,tune_type="jig")
        assert len(qs) == 2, "Should pull only 2 of 5 tunes that are jigs"
        assert (self.tune1 in qs) == False, "Should not contain tune1"
        assert (self.tune2 in qs) == False, "Should not contain tune2"
        assert (self.tune3 in qs) == False, "Should not contain tune3"
        assert (self.tune4 in qs) == True, "Should contain tune4"
        assert (self.tune5 in qs) == True, "Should contain tune5"
    
    def test_combine_abc(self, setup_data):
        qs = tunes_combine.pull_tunes(num=3, tune_type="reel")
        abc_text = tunes_combine.combine_abc(qs)

        assert False == True, "Finish writting test"
