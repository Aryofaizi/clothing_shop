from store import models

def categories(request):
    return {"categories": models.Category.objects.all()}