# tunes_combine.py

from tunes import models

def pull_tunes(num: int, tune_type: str):
    """
    Queries ABCTunes from database based on number needed

    Parameters
    ----------
        num (int): number of tunes to return
        tune_type (str): type of tune to return
    
    Returns
    -------
        QuerySet: From Tune model
    """

    qs = models.ABCTune.objects.filter(tune__tune_type__tune_type_char=tune_type).order_by('?')[:num]

    return qs

def combine_abc(qs):
    """
    Combine all abc text that is in qs (QuestSet)
    to create a complete set

    Parameters
    ----------
        qs (QuerySet): query set from models.ABCTune
    
    Returns
    -------
        str: Combined abc text from qs
    """

    abc_text_full = ""
    title = "T: "
    bpm = "Q:1/2=70" #TODO: Replace hardcoded bpm

    for abctune in qs:
        # Add Title of Tune, Part, and Key
        title += abctune.tune.name + " "
        abc_text_full += "P: " + abctune.tune.name + "\n"
        abc_text_full += "K: " + abctune.key.key_type_char + "\n"

        # Get ABCTunePieces For Individual ABCTune
        qs_pieces = models.ABCTunePiece.objects.filter(
            abc_tune__tune__pk = abctune.pk
        )
        # Build ABCPart Piece to Add
        for abc_part in qs_pieces:
            abc_text_full += abc_part.abc_piece + "\n"

    return title + "\n" + bpm + "\n" + abc_text_full