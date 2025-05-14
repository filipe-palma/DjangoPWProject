from django.contrib import admin

from .models import Pessoa

class PessoaAdmin (admin. ModelAdmin):
    list_display = ("nome", "idade",)
    ordering = ("nome", "idade",)
    search_fields = ("nome",)

admin.site.register(Pessoa, PessoaAdmin)
