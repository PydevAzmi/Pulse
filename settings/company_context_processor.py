# context processor
from .models import Company

def get_info(request):
    pulse = Company.objects.last()
    return {'pulse':pulse}