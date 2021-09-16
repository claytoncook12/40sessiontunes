import factory

from tunes.models import TuneType, Composer, Tune

class TuneTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = TuneType
        django_get_or_create = ('tune_type_char',) # Use if field has unique=True in model definition
    
    tune_type_char = "reel"

class ComposerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Composer
    
    name = "James McMahon"

class TuneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tune
    
    name = "The Banshee"
    tune_type = factory.SubFactory(TuneTypeFactory)
    parts = 2
    composer = factory.SubFactory(ComposerFactory)
    tune_info = """It was composed by James McMahon (b. ≈1900 – Dec. 1980 RIP),
                a flute player originally from South Fermanagh, in Northern Ireland."""