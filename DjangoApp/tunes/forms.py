# tunes/forms.py

from django import forms

class PullCombineABCForm(forms.Form):
    num_tunes = [
        ("1", 1),
        ("2", 2),
        ("3", 3),
    ]
    tune_type_choice = [
        ("reel", "reel"),
        ("jig", "jig"),
    ]
    num = forms.ChoiceField(
        choices=num_tunes,
        label= "Number",
        help_text= "Number of tunes to inlcude in generated abc"
    )
    tune_type = forms.ChoiceField(
        choices=tune_type_choice,
        label= "Tune Type",
    )