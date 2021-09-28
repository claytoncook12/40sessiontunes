# test_models.py
from django.conf import settings
from tunes.tests import factories
from tunes.models import WrongFileType

from django.core.exceptions import ValidationError

from pathlib import Path

from pydub import AudioSegment

import pytest

@pytest.mark.django_db
class TestTune:
    def test_init(self):
        obj = factories.TuneFactory()
        assert obj.pk == 1, "Should save an instance"

@pytest.mark.django_db
class TestMeter:
    def test_str(self):
        obj = factories.MeterFactory()
        assert str(obj) == "4/4", "Check __str__ method"

@pytest.mark.django_db
class TestUnitNoteLength:
    def test_str(self):
        obj = factories.UnitNoteLengthFactory()
        assert str(obj) == "1/8", "Check __str__ method"

@pytest.mark.django_db
class TestBPM:
    def test_str(self):
        obj = factories.BPMFactory()
        assert str(obj) == "BPM: 1/4=120", "Check __str__ method"
    
    def test_bpm_value(self):
        obj = factories.BPMFactory(bpm="1/4=120")
        assert obj.bpm_value == 120

@pytest.mark.django_db
class TestTune:
    def test_str(self):
        obj = factories.TuneFactory()
        assert str(obj) == "The Banshee (reel)", "Check __str__ method"
    
    def test_get_absolute_url(self):
        obj = factories.TuneFactory()

        assert "/tunes/1/" == obj.get_absolute_url(), "Check absolute url"

@pytest.mark.django_db
class TestABCTune:
    def test_init(self):
        obj = factories.ABCTuneFactory()
        assert obj.pk == 1, "Should save an instance"
    
    def test_str(self):
        obj = factories.ABCTuneFactory()
        assert str(obj) == "pk:1 The Banshee (reel) (G Major)"
    
    def test_abc_line_title(self):
        obj = factories.ABCTuneFactory(
            tune=factories.TuneFactory(name="Title")
        )
        assert obj.abc_line_title() == "T:Title", "Should contain ABC format of T:title"
    
    def test_abc_line_composer(self):
        obj = factories.ABCTuneFactory(
            tune=factories.TuneFactory(
                composer=factories.ComposerFactory(
                    name = "Test Name")
            )
        )
        assert obj.abc_line_composer() == "C:Test Name", "Should contain ABC format of C:composer_name"

        obj = factories.ABCTuneFactory(
            tune=factories.TuneFactory(
                composer=None
            )
        )

        assert obj.abc_line_composer() == "C:", "Shoud be blank for composer in ABC format"
    
    def test_abc_line_bpm(self):
        obj = factories.ABCTuneFactory(bpm=None)
        assert obj.abc_line_bpm() == ""   
        
        obj = factories.ABCTuneFactory(
            bpm=factories.BPMFactory(
                bpm='1/4=120'
            )
        )
        assert obj.abc_line_bpm() == "Q:1/4=120"     
    
    def test_abc_line_rhythm(self):
        obj = factories.ABCTuneFactory(
            tune = factories.TuneFactory(
                tune_type=factories.TuneTypeFactory(
                    tune_type_char = "reel"
                )
            )
        )
        assert obj.abc_line_rhythm() == "R:reel"

    def test_abc_default_notes(self):
        obj_abc_tune = factories.ABCTuneFactory()
        obj_abc_piece_1 = factories.ABCTunePieceFactory(
            abc_tune = obj_abc_tune,
            abc_piece = "|abcd|"
        )
        obj_abc_piece_2 = factories.ABCTunePieceFactory(
            abc_tune = obj_abc_tune,
            abc_piece = "|defg|"
        )

        assert obj_abc_tune.abc_default_notes() == "|abcd|\n|defg|\n"

    def test_abc_full_default_bpm(self):
        obj_abc_tune = factories.ABCTuneFactory()
        obj_abc_piece_1 = factories.ABCTunePieceFactory(
            abc_tune = obj_abc_tune,
            abc_piece = "|abcd|"
        )
        obj_abc_piece_2 = factories.ABCTunePieceFactory(
            abc_tune = obj_abc_tune,
            abc_piece = "|defg|"
        )
        abc_text_return = obj_abc_tune.abc_full_default_bpm()

        abc_correct = """T:The Banshee\nC:James McMahon\nR:reel\nM:4/4\nK:G Major\nL:1/8\nQ:1/4=120\n|abcd|\n|defg|\n"""

        assert abc_correct == abc_text_return, "ABC text should contain all header information"
    
    def test_abc_full_default(self):
        obj_abc_tune = factories.ABCTuneFactory()
        obj_abc_piece_1 = factories.ABCTunePieceFactory(
            abc_tune = obj_abc_tune,
            abc_piece = "|abcd|"
        )
        obj_abc_piece_2 = factories.ABCTunePieceFactory(
            abc_tune = obj_abc_tune,
            abc_piece = "|defg|"
        )
        abc_text_return = obj_abc_tune.abc_full_default()

        abc_correct = """T:The Banshee\nC:James McMahon\nR:reel\nM:4/4\nK:G Major\nL:1/8\n|abcd|\n|defg|\n"""
        
        assert abc_correct == abc_text_return, "ABC text should contain all header information except bpm"

    def test_abc_piece_and_bars(self):
        """
        Return abc text from ABCTune model with varying number
        of bars returned
        """
        obj_abc_tune = factories.ABCTuneFactory()

        # If no abc text for ABCTune
        assert obj_abc_tune.abc_piece_and_bars(1,2) == None, "If no abc test entered for ABCTune then return None"

        obj_abc_piece = factories.ABCTunePieceFactory(
            abc_tune = obj_abc_tune,
            part_order = 1,
            abc_piece = "|:~G3D EDB,D|GFGB d2Bd|eged BAGA|BAGE EDDE:|"
        )
        assert obj_abc_tune.abc_piece_and_bars(1, 1) == "|~G3D EDB,D|", "Return one abc text bar"
        assert obj_abc_tune.abc_piece_and_bars(1, 2) == "|~G3D EDB,D|GFGB d2Bd|", "Return two abc text bars"
        assert obj_abc_tune.abc_piece_and_bars(1, 3) == "|~G3D EDB,D|GFGB d2Bd|eged BAGA|", "Return two abc text bars"

        # If more bars than in tune
        with pytest.raises(ValueError):
            obj_abc_tune.abc_piece_and_bars(1,5) == ValueError, \
            "Shoud return error since more bars are requested than in abc text"

@pytest.mark.django_db
class TestABCTunePiece:
    def test_init(self):
        obj = factories.ABCTunePieceFactory()
        assert obj.pk == 1, "Should save an instance"

@pytest.mark.django_db
class TestReferenceAudio:
    def test_str(self):
        obj = factories.ReferenceAudioFactory()
        assert str(obj) == "Ref Audio: reel, 2 parts, 3 repeats, 1/4=120 BPM", "Check obj string"
    
    def test_init(self):
        obj = factories.ReferenceAudioFactory()
        assert obj.pk == 1, "Should save an instance"

        # Check varing properties about default file
        # Size in bytes
        assert obj.audio_file.size == 2963329, "Should be able to check audio file size"

        # Length of Audio Track in milliseconds
        assert obj.audio_file_length_milliseconds_round == 185143, "Length of time in milliseconds of mp3 file"
    
    def test_clean(self):
        with pytest.raises(ValidationError):
            obj = factories.ReferenceAudioFactory(
                audio_file = str(Path(settings.MEDIA_ROOT) / "fixtures" / "tunes" / "referenceaudio" / "test.wav")
            )
            obj.clean(), "Should raise error on clean due to file type not being .mp3"
    
    def test_buffer_end_time(self):
        obj1 = factories.ReferenceAudioFactory()
        assert obj1.buffer_end_time == 4000.00, "BPM 120 and beats_buffer is 8, so 4000 milliseconds"

        obj2 = factories.ReferenceAudioFactory(
            beats_buffer = 0,
            bpm = factories.BPMFactory(
                bpm = "1/8=60"
            )
        )
        assert obj2.buffer_end_time == 0, "BPM 60 and beats buffer is 0, so 0 milliseconds"
    
    def test_countin_end_time(self):
        obj1 = factories.ReferenceAudioFactory()
        assert obj1.countin_end_time == 8000, "BPM 120 and beats_buffer is 8, beats_countin is 8, so 8000 milliseconds"

        obj2 = factories.ReferenceAudioFactory(
            beats_buffer = 0,
            beats_countin = 0,
            bpm = factories.BPMFactory(
                bpm = "1/8=60"
            )
        )
        assert obj2.countin_end_time == 0, "BPM 120 and beats_buffer is 0, beats_countin is 0, so 8000 milliseconds"
    
    def test_get_start_firstpart_xtime(self):
        obj = factories.ReferenceAudioFactory()

        first_time = obj.get_start_firstpart_xtime(1)
        second_time = obj.get_start_firstpart_xtime(2)
        third_time = obj.get_start_firstpart_xtime(3)

        assert first_time == 8000, "Start of first time through tune"
        assert second_time == 24000, "Start of second time through tune"
        assert third_time == 40000, "Start of third time through tune"
