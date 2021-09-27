from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Tune, ABCTune
from .forms import PullCombineABCForm
from .tunes_combine import pull_tunes, combine_abc


# Create your views here.
def list(request):

    qs = Tune.objects.all()

    context = {
        "tunes" : qs
    }

    return render(request, 'tunes/list.html', context)

def detail(request, id):

    tune = get_object_or_404(Tune, pk=id)
    abc_qs = ABCTune.objects.filter(tune=tune)

    context = {
        "tune": tune,
        "abc_list": abc_qs,
    }

    return render(request, 'tunes/detail.html', context)

def abc_combine(request):

    if request.method == "GET":
        if 'num' in request.GET:
            if 'tune_type' in request.GET:
                form = PullCombineABCForm(request.GET)
                if form.is_valid():
                    abc = combine_abc(
                        pull_tunes(
                            num=int(form.cleaned_data['num']),
                            tune_type=form.cleaned_data['tune_type']
                        )
                    )

                    context = {
                        'form': form,
                        'abc': abc,
                    }

                    return render(request, 'tunes/abc_combine.html', context)

        else:
            form = PullCombineABCForm()

    return render(request, 'tunes/abc_combine.html', {'form': form})