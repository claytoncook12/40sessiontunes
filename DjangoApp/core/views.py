from django.shortcuts import render

# Create your views here.
def home(request):

    return render(request, 'home.html')

def midiexample_1(request):

    return render(request, 'midiexample_1.html')

def midiexample_2(request):

    return render(request, 'midiexample_2.html')