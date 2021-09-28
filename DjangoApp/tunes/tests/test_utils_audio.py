from tunes.utils_audio import mspb

def test_mspb():
    assert mspb(60) == 1000, "Check 60 bpm is 1000 milliseconds"