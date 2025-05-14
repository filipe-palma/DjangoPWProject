# noobsite/views.py

from django.http import HttpResponse

def index_view(request):
    return HttpResponse("Olá n00b, esta é a página web mais básica do mundo!")
    
def index_view2(request):
    return HttpResponse("Observa o simples que é!")
    
def index_view3(request):
    return HttpResponse("Que básico!")
    
def index_view4(request):
    return HttpResponse("Muito noob!")