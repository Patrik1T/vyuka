from django.shortcuts import render
from .models import Film

def index(request):
    context = {
        'predmet': Film.objects.order_by('-rate').all()[:3],
    }
    return render(request, 'index.html', context=context)
