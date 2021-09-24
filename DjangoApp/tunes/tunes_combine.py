# tunes_combine.py

from tunes import models

def pull_tunes(num: int, tune_type: str):
    """
    Queries Tunes from database based on number needed

    Parameters
    ----------
        num (int): number of tunes to return
        tune_type (str): type of tune to return
    
    Returns
    -------
        QuerySet: set that matches parameters
    """

    qs = models.Tune.objects.filter(tune_type__tune_type_char=tune_type).order_by('?')[:num]

    return qs