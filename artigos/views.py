from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.shortcuts import get_object_or_404, redirect
from .models import Artigo
from .forms import ArtigoForm, ComentarioForm, AvaliacaoForm

class ArtigoListView(generic.ListView):
    model = Artigo
    template_name = 'artigos/artigo_list.html'
    context_object_name = 'artigos'
    paginate_by = 10

class ArtigoDetailView(generic.DetailView):
    model = Artigo
    template_name = 'artigos/artigo_detail.html'
    context_object_name = 'artigo'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comentarios'] = self.object.comentarios.filter(aprovado=True)
        ctx['form_comentario'] = ComentarioForm()
        ctx['avaliacoes'] = self.object.avaliacoes.all()
        ctx['form_avaliacao'] = AvaliacaoForm()
        return ctx

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        if 'submit_comentario' in request.POST:
            form = ComentarioForm(request.POST)
            if form.is_valid():
                com = form.save(commit=False)
                com.artigo = self.object
                com.save()
            return redirect(self.object)
        if 'submit_avaliacao' in request.POST:
            form = AvaliacaoForm(request.POST)
            if form.is_valid():
                aval = form.save(commit=False)
                aval.artigo = self.object
                aval.save()
            return redirect(self.object)
        return super().get(request, *args, **kwargs)

class ArtigoCreateView(generic.CreateView):
    model = Artigo
    form_class = ArtigoForm
    template_name = 'artigos/artigo_form.html'

    def get_success_url(self):
        return reverse('artigo-detail', args=[self.object.slug])

class ArtigoUpdateView(generic.UpdateView):
    model = Artigo
    form_class = ArtigoForm
    template_name = 'artigos/artigo_form.html'

    def get_success_url(self):
        return reverse('artigo-detail', args=[self.object.slug])

class ArtigoDeleteView(generic.DeleteView):
    model = Artigo
    template_name = 'artigos/artigo_confirm_delete.html'
    success_url = reverse_lazy('artigo-list')


# Create your views here.
