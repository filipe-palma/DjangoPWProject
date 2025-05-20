from .models import Visitor

def visitor_count(request):
    return {
        'visitor_count': Visitor.get_total_count()
    }