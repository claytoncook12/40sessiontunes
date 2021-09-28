import pytest

from tunes.utils_audio import mspb, bpm_beats_to_milliseconds

def test_mspb():
    assert mspb(60) == 1000, "Check 60 bpm is 1000 milliseconds"

    with pytest.raises(ValueError):
        mspb(-1), "Check that negative bpm raises value error"

def test_bpm_beats_to_milliseconds():
    assert bpm_beats_to_milliseconds(70, 7) == 6000, "Check 70 bpm and 7 beats is 6000 milliseconds"
    assert bpm_beats_to_milliseconds(90, 3) == 2000, "Check 90 bpm and 3 beats is 2000 milliseconds"
    assert bpm_beats_to_milliseconds(102, 6) == 3529.41, "Check 102 bpm and 6 beats is 3529.41 milliseconds"
    assert bpm_beats_to_milliseconds(0, 0) == 0, "Check 0 bpm and 0 beats is 0 milliseconds"

    with pytest.raises(ValueError):
        bpm_beats_to_milliseconds(-1, 1), "Check that negative bpm raises value error"
    
    with pytest.raises(ValueError):
        bpm_beats_to_milliseconds(1, -1), "Check that negative beats raises value error"