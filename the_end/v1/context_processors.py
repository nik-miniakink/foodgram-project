from .models import Tag


def tags(request):
    tags = Tag.objects.all()
    context = {
        'tags': tags,
    }
    return context
