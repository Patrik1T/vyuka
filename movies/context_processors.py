from .models import Genre

def genres(request):
    return {'predmety': Genre.objects.all()}