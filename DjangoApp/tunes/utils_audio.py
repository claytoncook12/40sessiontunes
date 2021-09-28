def mspb(beats_per_minute: int) -> float:
    """
    Calculates milliseconds per beat from beats per minute
    Parameters
    ----------
        beats_per_minute (int or float)
    Returns
    -------
        float: seconds per beat
    """

    if beats_per_minute < 0:
        raise ValueError("Beats per minute must be greater than or equal to 0")
    
    if beats_per_minute == 0:
        return 0

    bpm = float(beats_per_minute)

    return (60/bpm)*1000

def bpm_beats_to_milliseconds(bpm: int, beats: int) -> float:
    """
    Calculates milliseconds from beats per minute
    and number of beats

    Parameters
    ----------
        bpm (int): beats per minute
        beats (int): beats
    
    Return
    ------
        float: milliseconds of time passed for beats to the hundreth place
    """
    
    if bpm < 0 or beats < 0:
        raise ValueError("BPM and Beats must both be zero or postive values.")

    return round(mspb(bpm) * beats, 2) 
