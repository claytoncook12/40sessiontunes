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

    bpm = float(beats_per_minute)

    return (60/bpm)*1000