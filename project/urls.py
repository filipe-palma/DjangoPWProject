

# urls.py

from django.contrib import admin
from django.urls import path, include   # incluir include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('noobsite/', include('noobsite.urls')),  # novo path
    path('portfolio/', include('portfolio.urls')),  # novo path
    path('artigos/', include('artigos.urls')),
    path('autenticacao/', include('autenticacao.urls')),
    path('accounts/', include('allauth.urls')),
]
