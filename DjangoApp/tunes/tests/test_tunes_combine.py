# test_tunes_combine.py

from tunes.tests import factories
from tunes import models

import pytest

from tunes import tunes_combine

@pytest.mark.django_db
class Test:
    @pytest.fixture
    def setup_data(self):
        # Create 5 tunes, abctune, and abctext for database
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
            abc_piece = "|efgA|"    
        )
        
        self.tune2 = factories.TuneFactory(
            name = "Tune 2",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "reel"
            )
        )
        self.abctune2 = factories.ABCTuneFactory(
            tune = self.tune2
        )
        self.abctune2peice1 = factories.ABCTunePieceFactory(
            abc_tune = self.abctune2,
            part_order = 1,
            part_title = "Part 1",
            abc_piece = "|ABCD|"    
        )
        self.abctune2peice2 = factories.ABCTunePieceFactory(
            abc_tune = self.abctune2,
            part_order = 2,
            part_title = "Part 2",
            abc_piece = "|EFGa|"    
        )

        self.tune3 = factories.TuneFactory(
            name = "Tune 3",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "reel"
            )
        )
        self.abctune3 = factories.ABCTuneFactory(
            tune = self.tune3
        )
        self.abctune3peice1 = factories.ABCTunePieceFactory(
            abc_tune = self.abctune3,
            part_order = 1,
            part_title = "Part 1",
            abc_piece = "|aaaa|"    
        )
        self.abctune3peice2 = factories.ABCTunePieceFactory(
            abc_tune = self.abctune3,
            part_order = 2,
            part_title = "Part 2",
            abc_piece = "|bbbb|"    
        )

        self.tune4 = factories.TuneFactory(
            name = "Tune 4",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "jig"
            )
        )
        self.abctune4 = factories.ABCTuneFactory(
            tune = self.tune4,
            meter = factories.MeterFactory(
                meter_type_char = "6/8"
            )
        )
        self.abctune4peice1 = factories.ABCTunePieceFactory(
            abc_tune = self.abctune4,
            part_order = 1,
            part_title = "Part 1",
            abc_piece = "|aaa aaa|"    
        )
        self.abctune4peice2 = factories.ABCTunePieceFactory(
            abc_tune = self.abctune4,
            part_order = 2,
            part_title = "Part 2",
            abc_piece = "|bbb bbb|"    
        )

        self.tune5 = factories.TuneFactory(
            name = "Tune 5",
            tune_type = factories.TuneTypeFactory(
                tune_type_char = "jig"
            )
        )
        self.abctune5 = factories.ABCTuneFactory(
            tune = self.tune5,
            meter = factories.MeterFactory(
                meter_type_char = "6/8"
            )
        )
        self.abctune5peice1 = factories.ABCTunePieceFactory(
            abc_tune = self.abctune5,
            part_order = 1,
            part_title = "Part 1",
            abc_piece = "|ccc ccc|"    
        )
        self.abctune5peice2 = factories.ABCTunePieceFactory(
            abc_tune = self.abctune5,
            part_order = 2,
            part_title = "Part 2",
            abc_piece = "|ddd ddd|"    
        )

    def test_pull_tunes(self, setup_data):
        # Check that queryset returns correct objects
        qs = tunes_combine.pull_tunes(num=3,tune_type="reel")
        assert len(qs) == 3, "Should pull only 3 of 5 tunes that are reels"
        assert (self.abctune1 in qs) == True, "Should contain abctune1"
        assert (self.abctune2 in qs) == True, "Should contain abctune2"
        assert (self.abctune3 in qs) == True, "Should contain abctune3"
        assert (self.abctune4 in qs) == False, "Should not contain abctune4"
        assert (self.abctune5 in qs) == False, "Should not contain abctune5"
        
        # Check that queryset returns correct objects
        qs = tunes_combine.pull_tunes(num=2,tune_type="jig")
        assert len(qs) == 2, "Should pull only 2 of 5 tunes that are jigs"
        assert (self.abctune1 in qs) == False, "Should not contain abctune1"
        assert (self.abctune2 in qs) == False, "Should not contain abctune2"
        assert (self.abctune3 in qs) == False, "Should not contain abctune3"
        assert (self.abctune4 in qs) == True, "Should contain abctune4"
        assert (self.abctune5 in qs) == True, "Should contain abctune5"
    
    def test_combine_abc(self, setup_data):
        qs = tunes_combine.pull_tunes(num=3, tune_type="reel")
        abc_text, title = tunes_combine.combine_abc(qs)

        assert "P: Tune 1\nK: G Major\nM: 4/4\n|abcd|\n|efgA|\n" in abc_text, "abctune1 piece 1 and 2 in abc_text output"
        assert "P: Tune 2\nK: G Major\nM: 4/4\n|ABCD|\n|EFGa|\n" in abc_text, "abctune2 piece 1 and 2 in abc_text output"
        assert "P: Tune 3\nK: G Major\nM: 4/4\n|aaaa|\n|bbbb|\n" in abc_text, "abctune2 piece 1 and 2 in abc_text output"

        qs = tunes_combine.pull_tunes(num=2, tune_type="jig")
        abc_text, title = tunes_combine.combine_abc(qs)

        assert "P: Tune 4\nK: G Major\nM: 6/8\n|aaa aaa|\n|bbb bbb|\n" in abc_text, "abctune4 piece 1 and 2 in abc_text output"
        assert "P: Tune 5\nK: G Major\nM: 6/8\n|ccc ccc|\n|ddd ddd|\n" in abc_text, "abctune5 piece 1 and 2 in abc_text output"
