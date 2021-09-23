# tunes_combine.py

from tunes import models

def pull_tunes(num,tune_type):
    """
    Queries tunes from database based on number needed and
    tune_type specified
    """

    qs = models.Tune.objects.filter(tune_type__tune_type_char=tune_type).order_by('?')[:num]

    return qs