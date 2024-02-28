
from . import models


def categories(request):
    """Get categories list."""
    return {"categories": models.Category.objects.all()}
