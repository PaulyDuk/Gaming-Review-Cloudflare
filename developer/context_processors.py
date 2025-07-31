from .models import Developer

def developers_context(request):
    return {'all_developers': Developer.objects.all()}
