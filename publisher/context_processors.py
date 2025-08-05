from .models import Publisher


def publishers_context(request):
    return {'all_publishers': Publisher.objects.all()}
