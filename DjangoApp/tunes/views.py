from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Tune, ABCTune


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