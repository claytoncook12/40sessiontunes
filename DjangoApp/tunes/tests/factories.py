import factory
from pathlib import Path

from django.conf import settings
from tunes import models

class TuneTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.TuneType
        django_get_or_create = ('tune_type_char',) # Use if field has unique=True in model definition
    
    tune_type_char = "reel"

class KeyFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Key
        django_get_or_create = ('key_type_char',)
    
    key_type_char = "G Major"

class MeterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Meter
        django_get_or_create = ('meter_type_char',)
    
    meter_type_char = "4/4"

class ComposerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Composer
    
    name = "James McMahon"

class UnitNoteLengthFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.UnitNoteLength
        django_get_or_create = ('unit_note_length',)
    
    unit_note_length = "1/8"

class BPMFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.BPM
        django_get_or_create = ('bpm',)
    
    bpm = "1/4=120"

class TuneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Tune
    
    name = "The Banshee"
    tune_type = factory.SubFactory(TuneTypeFactory)
    parts = 2
    composer = factory.SubFactory(ComposerFactory)
    tune_info = """It was composed by James McMahon (b. ≈1900 – Dec. 1980 RIP),
                a flute player originally from South Fermanagh, in Northern Ireland."""

class ABCTuneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ABCTune
    
    tune = factory.SubFactory(TuneFactory)
    key = factory.SubFactory(KeyFactory)
    meter = factory.SubFactory(MeterFactory)
    unit_note_length = factory.SubFactory(UnitNoteLengthFactory)
    bpm = factory.SubFactory(BPMFactory)

class ABCTunePieceFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ABCTunePiece
    
    abc_tune = factory.SubFactory(ABCTuneFactory)
    part_order = 1
    part_title = "Part 1"
    default = True
    abc_piece = """
                "G"~G3D EDB,D|GFGB d2Bd|"C"eged BAGA|"G"BAGE "D"EDDE|
                "G"~G3D EDB,D|GFGB d2Bd|"C"eged BAGA|"G"BAGE "D"EDD2:|
                """

class ReferenceAudioFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ReferenceAudio
    
    tune_type = factory.SubFactory(TuneTypeFactory)
    bpm = factory.SubFactory(BPMFactory)
    parts = 2
    repeats = 3
    meter = factory.SubFactory(MeterFactory)
    beats_buffer = 8
    beats_countin = 8
    beats_ending = 8
    beats_per_part = 32
    audio_file = str(Path(settings.MEDIA_ROOT) / "ReferenceAudio" / "Reel-2Part-3Repeats-70BPM.mp3")
    description = "refernce file of reel, 2 parts, 3 repeats, 3/8=70 BPM"